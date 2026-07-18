from collections import defaultdict

from client_customizations.consignment.infrastructure.frappe_adapter import (
	db_get_value,
	db_set_value,
	get_doc,
	get_list,
)


SKIP_REASON_MISSING_SUPPLIER = "MISSING_SUPPLIER"
SKIP_REASON_MISSING_ITEM = "MISSING_ITEM"
SKIP_REASON_ALREADY_SETTLED = "ALREADY_SETTLED"
SKIP_REASON_EXISTING_DRAFT = "EXISTING_DRAFT"
SKIP_REASON_SOURCE_LINKED_TO_OTHER_SETTLEMENT = "SOURCE_LINKED_TO_OTHER_SETTLEMENT"


SETTLEMENT_ROW_SCHEMA_KEYS = (
	"sales_doctype",
	"sales_document",
	"sales_row",
	"supplier",
	"item_code",
	"qty",
	"base_amount",
	"custom_consignment_settlement",
)


def normalize_settlement_row(
	row,
	default_sales_doctype=None,
	default_sales_document=None,
	default_supplier=None,
	amount_field_candidates=None,
):
	"""Normalize incoming sales rows into one canonical schema for settlement flows."""
	amount_candidates = list(amount_field_candidates or []) + ["base_amount", "base_net_amount"]
	amount = 0.0
	for fieldname in amount_candidates:
		if row.get(fieldname) is not None:
			amount = float(row.get(fieldname) or 0)
			break

	return {
		"sales_doctype": row.get("sales_doctype") or row.get("doctype") or default_sales_doctype,
		"sales_document": row.get("sales_document") or row.get("parent") or default_sales_document,
		"sales_row": row.get("sales_row") or row.get("name"),
		"supplier": row.get("supplier") or row.get("custom_consignment_supplier") or default_supplier,
		"item_code": row.get("item_code"),
		"qty": float(row.get("qty") or 0),
		"base_amount": amount,
		"custom_consignment_settlement": row.get("custom_consignment_settlement"),
	}


def classify_row_skip_reason(row):
	"""Pure helper to map canonical row state to an optional skip reason code."""
	normalized_row = normalize_settlement_row(row)
	if normalized_row.get("custom_consignment_settlement"):
		return SKIP_REASON_ALREADY_SETTLED
	if not normalized_row.get("supplier"):
		return SKIP_REASON_MISSING_SUPPLIER
	if not normalized_row.get("item_code"):
		return SKIP_REASON_MISSING_ITEM
	return None


def partition_settlement_rows_with_reasons(rows):
	"""Pure helper to partition rows into accepted canonical rows and reason-coded skips."""
	accepted = []
	skipped = []

	for row in rows or []:
		normalized_row = normalize_settlement_row(row)
		reason_code = classify_row_skip_reason(normalized_row)
		if reason_code:
			skipped.append(
				{
					"reason_code": reason_code,
					"sales_doctype": normalized_row.get("sales_doctype"),
					"sales_document": normalized_row.get("sales_document"),
					"sales_row": normalized_row.get("sales_row"),
					"supplier": normalized_row.get("supplier"),
					"item_code": normalized_row.get("item_code"),
				}
			)
			continue

		accepted.append(normalized_row)

	return accepted, skipped


def aggregate_skip_reasons(skipped_rows_or_entries):
	"""Pure helper to aggregate reason-coded skip entries into a compact counter map."""
	counts = defaultdict(int)
	for row in skipped_rows_or_entries or []:
		reason_code = row.get("reason_code")
		if reason_code:
			counts[reason_code] += 1
	return dict(counts)


def get_sold_not_settled_summary(company, supplier=None, posting_date_from=None, posting_date_to=None):
	"""Fetch submitted consignment sale rows and aggregate unsettled quantities and amounts."""
	filters = {
		"docstatus": 1,
		"company": company,
		"custom_is_consignment": 1,
	}

	if supplier:
		filters["custom_consignment_supplier"] = supplier

	if posting_date_from and posting_date_to:
		filters["posting_date"] = ["between", [posting_date_from, posting_date_to]]

	rows = get_list(
		"Sales Invoice Item",
		fields=["item_code", "qty", "base_net_amount", "custom_consignment_settlement"],
		filters=filters,
		order_by="item_code asc",
	)
	return aggregate_sold_not_settled_rows(rows)


def fetch_unsettled_sale_rows(company, posting_date, supplier=None):
	"""Fetch submitted unsettled consignment rows from Sales Invoice and Delivery Note."""
	rows = []
	rows.extend(_fetch_unsettled_rows_for_sales_doctype("Sales Invoice", company, posting_date, supplier))
	rows.extend(_fetch_unsettled_rows_for_sales_doctype("Delivery Note", company, posting_date, supplier))
	return rows


def _fetch_unsettled_rows_for_sales_doctype(sales_doctype, company, posting_date, supplier=None):
	sale_filters = {
		"docstatus": 1,
		"company": company,
		"posting_date": posting_date,
		"custom_is_consignment": 1,
	}
	if supplier:
		sale_filters["custom_consignment_supplier"] = supplier

	sales_docs = get_list(
		sales_doctype,
		fields=["name", "custom_consignment_supplier"],
		filters=sale_filters,
		limit_page_length=0,
	)
	if not sales_docs:
		return []

	child_doctype = f"{sales_doctype} Item"
	amount_field = "base_net_amount" if sales_doctype == "Sales Invoice" else "base_amount"
	parents = [row.get("name") for row in sales_docs if row.get("name")]
	parent_supplier_map = {
		row.get("name"): row.get("custom_consignment_supplier")
		for row in sales_docs
		if row.get("name")
	}

	item_rows = get_list(
		child_doctype,
		fields=[
			"name",
			"parent",
			"item_code",
			"qty",
			amount_field,
			"custom_consignment_supplier",
			"custom_consignment_settlement",
			"custom_is_consignment",
		],
		filters={
			"parent": ["in", parents],
			"custom_is_consignment": 1,
		},
		limit_page_length=0,
	)

	normalized = []
	for row in item_rows:
		normalized_row = normalize_settlement_row(
			row,
			default_sales_doctype=sales_doctype,
			default_sales_document=row.get("parent"),
			default_supplier=parent_supplier_map.get(row.get("parent")),
			amount_field_candidates=[amount_field],
		)
		if _is_unsettled_row(normalized_row):
			normalized.append(normalized_row)

	return normalized


def _is_unsettled_row(row):
	return not row.get("custom_consignment_settlement")


def group_rows_by_supplier_item(rows):
	"""Pure helper to group normalized rows by supplier + item_code."""
	grouped = defaultdict(
		lambda: {
			"supplier": None,
			"item_code": None,
			"qty": 0.0,
			"base_amount": 0.0,
			"source_rows": [],
		}
	)

	for row in rows or []:
		normalized_row = normalize_settlement_row(row)
		reason_code = classify_row_skip_reason(normalized_row)
		if reason_code:
			continue

		supplier = normalized_row.get("supplier")
		item_code = normalized_row.get("item_code")

		key = (supplier, item_code)
		entry = grouped[key]
		entry["supplier"] = supplier
		entry["item_code"] = item_code
		entry["qty"] += float(normalized_row.get("qty") or 0)
		entry["base_amount"] += float(normalized_row.get("base_amount") or 0)
		entry["source_rows"].append(
			{
				"sales_doctype": normalized_row.get("sales_doctype"),
				"sales_document": normalized_row.get("sales_document"),
				"sales_row": normalized_row.get("sales_row"),
				"supplier": supplier,
				"item_code": item_code,
				"qty": float(normalized_row.get("qty") or 0),
				"base_amount": float(normalized_row.get("base_amount") or 0),
			}
		)

	return list(grouped.values())


def split_grouped_lines_by_supplier(grouped_lines):
	"""Pure helper to bucket grouped lines per supplier for header creation."""
	buckets = defaultdict(list)
	for line in grouped_lines or []:
		supplier = line.get("supplier")
		if supplier:
			buckets[supplier].append(line)
	return dict(buckets)


def compute_totals_from_lines(lines):
	"""Pure helper to compute total quantity and amount for a line list."""
	total_qty = 0.0
	total_amount = 0.0
	for line in lines or []:
		total_qty += float(line.get("qty") or 0)
		total_amount += float(line.get("base_amount") or 0)
	return {"total_qty": total_qty, "total_amount": total_amount}


def should_create_draft_for_supplier(supplier, posting_date, existing_supplier_date_keys):
	"""Pure idempotency helper: create only if supplier+date key is absent."""
	return (supplier, posting_date) not in set(existing_supplier_date_keys or [])


def generate_draft_settlements_for_date(company, posting_date, supplier=None, dry_run=False, include_summary=False):
	"""Create draft settlements for one day from unsettled rows with idempotency guard."""
	rows = fetch_unsettled_sale_rows(company=company, posting_date=posting_date, supplier=supplier)
	accepted_rows, skipped_rows = partition_settlement_rows_with_reasons(rows)
	grouped_lines = group_rows_by_supplier_item(accepted_rows)
	buckets = split_grouped_lines_by_supplier(grouped_lines)
	all_skipped_entries = list(skipped_rows)
	if not buckets:
		if include_summary:
			return {
				"created": [],
				"created_count": 0,
				"skipped_count": len(all_skipped_entries),
				"skip_reason_counts": aggregate_skip_reasons(all_skipped_entries),
			}
		return []

	settlement_filters = {
		"company": company,
		"posting_date": posting_date,
		"status": "Draft",
	}
	if supplier:
		settlement_filters["supplier"] = supplier

	existing_drafts = get_list(
		"Consignment Settlement",
		fields=["name", "supplier", "posting_date"],
		filters=settlement_filters,
		limit_page_length=0,
	)
	existing_keys = {
		(row.get("supplier"), str(row.get("posting_date")))
		for row in existing_drafts
		if row.get("supplier") and row.get("posting_date")
	}

	created = []
	skipped_count = 0
	for supplier_name, supplier_lines in buckets.items():
		if not should_create_draft_for_supplier(supplier_name, str(posting_date), existing_keys):
			skipped_count += 1
			all_skipped_entries.append(
				{
					"reason_code": SKIP_REASON_EXISTING_DRAFT,
					"supplier": supplier_name,
					"posting_date": str(posting_date),
				}
			)
			continue

		items = _build_settlement_items_from_grouped_lines(supplier_lines)
		if not items:
			skipped_count += 1
			continue

		settlement_doc = get_doc(
			{
				"doctype": "Consignment Settlement",
				"company": company,
				"supplier": supplier_name,
				"posting_date": posting_date,
				"status": "Draft",
				"items": items,
			}
		)
		if dry_run:
			created.append({"name": None, "supplier": supplier_name, "posting_date": posting_date, "items": items})
			continue

		settlement_doc.insert(ignore_permissions=True)
		marking_result = mark_source_rows_as_settled(items=items, settlement_name=settlement_doc.name, dry_run=dry_run)
		for reason_code, count in (marking_result.get("skip_reason_counts") or {}).items():
			for _ in range(int(count or 0)):
				all_skipped_entries.append({"reason_code": reason_code, "supplier": supplier_name})
		skipped_count += int(marking_result.get("skipped_count", 0))
		created.append(
			{
				"name": settlement_doc.name,
				"supplier": supplier_name,
				"posting_date": posting_date,
				"items": items,
			}
		)

	if include_summary:
		return {
			"created": created,
			"created_count": len(created),
			"skipped_count": skipped_count + len(skipped_rows),
			"skip_reason_counts": aggregate_skip_reasons(all_skipped_entries),
		}
	return created


def _build_settlement_items_from_grouped_lines(grouped_lines):
	items = []
	for line in grouped_lines or []:
		for source_row in line.get("source_rows") or []:
			if not source_row.get("sales_doctype") or not source_row.get("sales_document") or not source_row.get("sales_row"):
				continue
			items.append(
				{
					"sales_doctype": source_row.get("sales_doctype"),
					"sales_document": source_row.get("sales_document"),
					"sales_row": source_row.get("sales_row"),
					"supplier": source_row.get("supplier"),
					"item_code": source_row.get("item_code"),
					"qty": float(source_row.get("qty") or 0),
					"base_amount": float(source_row.get("base_amount") or 0),
				}
			)
	return items


def mark_source_rows_as_settled(items, settlement_name, dry_run=False):
	"""Mark source sales rows with settlement reference after successful insert."""
	if dry_run:
		return {"marked_count": 0, "skipped_count": 0, "skip_reason_counts": {}}

	seen = set()
	marked_count = 0
	skipped_count = 0
	skipped_entries = []
	for item in items or []:
		normalized_item = normalize_settlement_row(item)
		key = (normalized_item.get("sales_doctype"), normalized_item.get("sales_row"))
		if key in seen:
			skipped_count += 1
			continue
		seen.add(key)

		sales_doctype = normalized_item.get("sales_doctype")
		sales_row = normalized_item.get("sales_row")
		if not sales_doctype or not sales_row:
			skipped_count += 1
			continue

		source_row_doctype = f"{sales_doctype} Item"
		current_settlement = db_get_value(
			source_row_doctype,
			sales_row,
			"custom_consignment_settlement",
		)
		if current_settlement and current_settlement != settlement_name:
			skipped_count += 1
			skipped_entries.append(
				{
					"reason_code": SKIP_REASON_SOURCE_LINKED_TO_OTHER_SETTLEMENT,
					"sales_row": sales_row,
					"sales_doctype": sales_doctype,
					"existing_settlement": current_settlement,
				}
			)
			continue
		if current_settlement == settlement_name:
			skipped_count += 1
			skipped_entries.append(
				{
					"reason_code": SKIP_REASON_ALREADY_SETTLED,
					"sales_row": sales_row,
					"sales_doctype": sales_doctype,
				}
			)
			continue

		db_set_value(source_row_doctype, sales_row, "custom_consignment_settlement", settlement_name)
		marked_count += 1

	return {
		"marked_count": marked_count,
		"skipped_count": skipped_count,
		"skip_reason_counts": aggregate_skip_reasons(skipped_entries),
	}


def aggregate_sold_not_settled_rows(rows):
	"""Pure aggregation helper for sold-not-settled lines."""
	totals_by_item = defaultdict(lambda: {"qty": 0.0, "amount": 0.0})
	total_qty = 0.0
	total_amount = 0.0

	for row in rows:
		if row.get("custom_consignment_settlement"):
			continue

		item_code = row.get("item_code") or "UNKNOWN"
		qty = float(row.get("qty") or 0)
		amount = float(row.get("base_net_amount") or 0)

		totals_by_item[item_code]["qty"] += qty
		totals_by_item[item_code]["amount"] += amount
		total_qty += qty
		total_amount += amount

	return {
		"total_qty": total_qty,
		"total_amount": total_amount,
		"by_item": dict(totals_by_item),
	}


def build_draft_settlement_lines(rows):
	"""Build draft settlement line payloads from raw rows using canonical schema normalization."""
	normalized_rows, _ = partition_settlement_rows_with_reasons(rows)

	return group_rows_by_supplier_item(normalized_rows)


def should_clear_source_row_link(current_settlement, settlement_name):
	"""Pure helper for idempotent reversal behavior on settlement cancellation."""
	return bool(current_settlement and current_settlement == settlement_name)


def clear_source_rows_settlement_link(items, settlement_name, dry_run=False):
	"""Clear source-row settlement links when linked to this exact settlement only."""
	if dry_run:
		return {"cleared_count": 0, "skipped_count": 0, "skip_reason_counts": {}}

	seen = set()
	cleared_count = 0
	skipped_count = 0
	skipped_entries = []

	for item in items or []:
		normalized_item = normalize_settlement_row(item)
		key = (normalized_item.get("sales_doctype"), normalized_item.get("sales_row"))
		if key in seen:
			skipped_count += 1
			continue
		seen.add(key)

		sales_doctype = normalized_item.get("sales_doctype")
		sales_row = normalized_item.get("sales_row")
		if not sales_doctype or not sales_row:
			skipped_count += 1
			continue

		source_row_doctype = f"{sales_doctype} Item"
		current_settlement = db_get_value(
			source_row_doctype,
			sales_row,
			"custom_consignment_settlement",
		)

		if should_clear_source_row_link(current_settlement, settlement_name):
			db_set_value(source_row_doctype, sales_row, "custom_consignment_settlement", "")
			cleared_count += 1
			continue

		skipped_count += 1
		if current_settlement and current_settlement != settlement_name:
			skipped_entries.append(
				{
					"reason_code": SKIP_REASON_SOURCE_LINKED_TO_OTHER_SETTLEMENT,
					"sales_doctype": sales_doctype,
					"sales_row": sales_row,
				}
			)
		else:
			skipped_entries.append(
				{
					"reason_code": SKIP_REASON_ALREADY_SETTLED,
					"sales_doctype": sales_doctype,
					"sales_row": sales_row,
				}
			)

	return {
		"cleared_count": cleared_count,
		"skipped_count": skipped_count,
		"skip_reason_counts": aggregate_skip_reasons(skipped_entries),
	}
