from collections import defaultdict

from client_customizations.consignment.application.settlement import (
	classify_row_skip_reason,
	normalize_settlement_row,
)
from client_customizations.consignment.infrastructure.frappe_adapter import get_list


EXPOSURE_STATUSES = ("Draft", "Submitted", "Cancelled")


def to_float(value):
	return float(value or 0)


def make_scope_filters(company, supplier=None, posting_date_from=None, posting_date_to=None):
	"""Pure helper to build parent document filters from report scope arguments."""
	filters = {
		"docstatus": 1,
		"company": company,
		"custom_is_consignment": 1,
	}
	if supplier:
		filters["custom_consignment_supplier"] = supplier
	if posting_date_from and posting_date_to:
		filters["posting_date"] = ["between", [posting_date_from, posting_date_to]]
	elif posting_date_from:
		filters["posting_date"] = [">=", posting_date_from]
	elif posting_date_to:
		filters["posting_date"] = ["<=", posting_date_to]
	return filters


def bucket_numeric_rows(rows, group_fields, qty_field="qty", amount_field="base_amount"):
	"""Pure helper to bucket rows by key fields and aggregate quantity/amount/count."""
	buckets = defaultdict(lambda: {"row_count": 0, "qty": 0.0, "amount": 0.0})

	for row in rows or []:
		key = tuple(row.get(fieldname) for fieldname in group_fields)
		entry = buckets[key]
		entry["row_count"] += 1
		entry["qty"] += to_float(row.get(qty_field))
		entry["amount"] += to_float(row.get(amount_field))

	result = []
	for key, entry in buckets.items():
		grouped = {fieldname: key[index] for index, fieldname in enumerate(group_fields)}
		grouped.update(entry)
		result.append(grouped)

	result.sort(key=lambda row: tuple(row.get(fieldname) or "" for fieldname in group_fields))
	return result


def build_sold_not_settled_dataset(rows, skipped_rows=None):
	"""Pure helper to compute sold-not-settled rollups by supplier/item and posting date."""
	by_supplier_item = bucket_numeric_rows(rows, ["supplier", "item_code"])
	by_posting_date = bucket_numeric_rows(rows, ["posting_date"])

	total_qty = sum(to_float(row.get("qty")) for row in rows or [])
	total_amount = sum(to_float(row.get("base_amount")) for row in rows or [])

	return {
		"total_qty": total_qty,
		"total_amount": total_amount,
		"row_count": len(rows or []),
		"by_supplier_item": by_supplier_item,
		"by_posting_date": by_posting_date,
		"skipped_count": len(skipped_rows or []),
	}


def build_settlement_status_exposure_dataset(rows):
	"""Pure helper to expose status counts and amounts by supplier+posting_date bucket."""
	by_supplier_date = defaultdict(
		lambda: {
			"supplier": None,
			"posting_date": None,
			"counts": {status: 0 for status in EXPOSURE_STATUSES},
			"amounts": {status: 0.0 for status in EXPOSURE_STATUSES},
		}
	)
	status_totals = {
		status: {"count": 0, "amount": 0.0}
		for status in EXPOSURE_STATUSES
	}

	for row in rows or []:
		status = row.get("status")
		if status not in EXPOSURE_STATUSES:
			continue

		supplier = row.get("supplier")
		posting_date = str(row.get("posting_date") or "")
		bucket_key = (supplier, posting_date)
		bucket = by_supplier_date[bucket_key]
		bucket["supplier"] = supplier
		bucket["posting_date"] = posting_date
		bucket["counts"][status] += 1
		bucket["amounts"][status] += to_float(row.get("total_amount"))

		status_totals[status]["count"] += 1
		status_totals[status]["amount"] += to_float(row.get("total_amount"))

	buckets = list(by_supplier_date.values())
	buckets.sort(key=lambda row: ((row.get("supplier") or ""), (row.get("posting_date") or "")))
	return {
		"by_supplier_date": buckets,
		"status_totals": status_totals,
	}


def get_sold_not_settled_summary_by_scope(
	company,
	supplier=None,
	item_code=None,
	posting_date_from=None,
	posting_date_to=None,
):
	"""Fetch sold-not-settled rows for scoped Sales Invoice and Delivery Note data."""
	all_rows = []
	all_skipped = []
	all_rows.extend(
		_fetch_unsettled_rows_for_sales_doctype_scope(
			"Sales Invoice",
			company=company,
			supplier=supplier,
			item_code=item_code,
			posting_date_from=posting_date_from,
			posting_date_to=posting_date_to,
		)
	)
	all_rows.extend(
		_fetch_unsettled_rows_for_sales_doctype_scope(
			"Delivery Note",
			company=company,
			supplier=supplier,
			item_code=item_code,
			posting_date_from=posting_date_from,
			posting_date_to=posting_date_to,
		)
	)

	accepted_rows = []
	for row in all_rows:
		reason_code = classify_row_skip_reason(row)
		if reason_code:
			all_skipped.append({"reason_code": reason_code, "row": row})
			continue
		accepted_rows.append(row)

	return {
		"scope": {
			"company": company,
			"supplier": supplier,
			"item_code": item_code,
			"posting_date_from": posting_date_from,
			"posting_date_to": posting_date_to,
		},
		"summary": build_sold_not_settled_dataset(accepted_rows, skipped_rows=all_skipped),
	}


def get_settlement_status_exposure(company, supplier=None, posting_date_from=None, posting_date_to=None):
	"""Fetch settlement status exposure by supplier and posting date."""
	filters = {"company": company}
	if supplier:
		filters["supplier"] = supplier
	if posting_date_from and posting_date_to:
		filters["posting_date"] = ["between", [posting_date_from, posting_date_to]]
	elif posting_date_from:
		filters["posting_date"] = [">=", posting_date_from]
	elif posting_date_to:
		filters["posting_date"] = ["<=", posting_date_to]

	rows = get_list(
		"Consignment Settlement",
		fields=["name", "supplier", "posting_date", "status", "total_amount"],
		filters=filters,
		limit_page_length=0,
	)

	return {
		"scope": {
			"company": company,
			"supplier": supplier,
			"posting_date_from": posting_date_from,
			"posting_date_to": posting_date_to,
		},
		"exposure": build_settlement_status_exposure_dataset(rows),
	}


def _fetch_unsettled_rows_for_sales_doctype_scope(
	sales_doctype,
	company,
	supplier=None,
	item_code=None,
	posting_date_from=None,
	posting_date_to=None,
):
	parent_filters = make_scope_filters(
		company=company,
		supplier=supplier,
		posting_date_from=posting_date_from,
		posting_date_to=posting_date_to,
	)
	parents = get_list(
		sales_doctype,
		fields=["name", "posting_date", "custom_consignment_supplier"],
		filters=parent_filters,
		limit_page_length=0,
	)
	if not parents:
		return []

	amount_field = "base_net_amount" if sales_doctype == "Sales Invoice" else "base_amount"
	parent_names = [row.get("name") for row in parents if row.get("name")]
	parent_scope = {
		row.get("name"): {
			"posting_date": row.get("posting_date"),
			"supplier": row.get("custom_consignment_supplier"),
		}
		for row in parents
		if row.get("name")
	}

	item_filters = {
		"parent": ["in", parent_names],
		"custom_is_consignment": 1,
	}
	if item_code:
		item_filters["item_code"] = item_code

	child_rows = get_list(
		f"{sales_doctype} Item",
		fields=[
			"name",
			"parent",
			"item_code",
			"qty",
			amount_field,
			"custom_consignment_supplier",
			"custom_consignment_settlement",
		],
		filters=item_filters,
		limit_page_length=0,
	)

	normalized_rows = []
	for row in child_rows:
		normalized = normalize_settlement_row(
			row,
			default_sales_doctype=sales_doctype,
			default_sales_document=row.get("parent"),
			default_supplier=(parent_scope.get(row.get("parent")) or {}).get("supplier"),
			amount_field_candidates=[amount_field],
		)
		if normalized.get("custom_consignment_settlement"):
			continue
		normalized["posting_date"] = str((parent_scope.get(row.get("parent")) or {}).get("posting_date") or "")
		normalized_rows.append(normalized)

	return normalized_rows
