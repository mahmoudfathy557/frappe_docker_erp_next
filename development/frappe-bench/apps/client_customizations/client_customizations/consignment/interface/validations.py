from client_customizations.consignment.infrastructure.frappe_adapter import (
	db_get_value,
	get_list,
	throw,
)


def validate_purchase_receipt_for_consignment(doc, method=None):
	"""V1 consignment checks for Purchase Receipt before save."""
	if not is_consignment_doc(doc):
		return

	supplier = getattr(doc, "supplier", None)
	if not supplier:
		throw("Consignment Purchase Receipt requires a Supplier.")

	if not db_get_value("Supplier", supplier, "name"):
		throw(f"Supplier {supplier} was not found.")

	missing_warehouses = get_items_missing_warehouse(getattr(doc, "items", []) or [])
	if missing_warehouses:
		rows = ", ".join(str(row) for row in missing_warehouses)
		throw(f"Consignment items require warehouse. Missing on rows: {rows}")


def validate_sale_posting_for_consignment(doc, method=None):
	"""V1 consignment checks for Delivery Note / Sales Invoice on submit."""
	if not is_consignment_doc(doc):
		return

	items = getattr(doc, "items", []) or []
	if not has_sale_items(items):
		throw("Consignment sale submit requires at least one item.")

	doc_supplier = getattr(doc, "custom_consignment_supplier", None)
	rows_without_supplier = get_rows_missing_supplier_link(items, doc_supplier)
	if rows_without_supplier:
		rows = ", ".join(str(row) for row in rows_without_supplier)
		throw(
			"Consignment supplier linkage is required on sale rows. "
			f"Missing on rows: {rows}"
		)


def get_sales_doc_child_doctype(sales_doctype):
	return f"{sales_doctype} Item"


def get_submitted_settlement_names(settlement_state_rows):
	"""Pure helper to keep cancellation decision deterministic in tests and runtime."""
	result = []
	for row in settlement_state_rows or []:
		docstatus = row.get("docstatus")
		status = row.get("status")
		name = row.get("name")
		if not name:
			continue
		if int(docstatus or 0) == 1 or status == "Submitted":
			result.append(name)
	return sorted(set(result))


def validate_sale_cancel_not_linked_to_submitted_settlement(doc, method=None):
	"""Block cancellation while source rows are linked to submitted settlements."""
	child_doctype = get_sales_doc_child_doctype(doc.doctype)
	linked_rows = get_list(
		child_doctype,
		fields=["custom_consignment_settlement"],
		filters={
			"parent": doc.name,
			"custom_consignment_settlement": ["!=", ""],
		},
		limit_page_length=0,
	)

	settlement_names = sorted(
		{
			row.get("custom_consignment_settlement")
			for row in linked_rows
			if row.get("custom_consignment_settlement")
		}
	)
	if not settlement_names:
		return

	settlement_state_rows = []
	for settlement_name in settlement_names:
		docstatus, status = db_get_value(
			"Consignment Settlement",
			settlement_name,
			["docstatus", "status"],
		) or (None, None)
		settlement_state_rows.append(
			{
				"name": settlement_name,
				"docstatus": docstatus,
				"status": status,
			}
		)

	submitted_names = get_submitted_settlement_names(settlement_state_rows)
	if submitted_names:
		throw(
			f"Cannot cancel {doc.doctype} {doc.name}. "
			"Linked to submitted Consignment Settlement(s): "
			f"{', '.join(submitted_names)}. "
			"Cancel those settlement(s) first to clear source links safely."
		)


def is_consignment_doc(doc) -> bool:
	return bool(getattr(doc, "custom_is_consignment", 0) or getattr(doc, "is_consignment", 0))


def has_sale_items(items) -> bool:
	return len(items or []) > 0


def get_items_missing_warehouse(items):
	missing_rows = []
	for index, item in enumerate(items or [], start=1):
		if not getattr(item, "warehouse", None):
			missing_rows.append(getattr(item, "idx", index))
	return missing_rows


def get_rows_missing_supplier_link(items, fallback_supplier=None):
	missing_rows = []
	for index, item in enumerate(items or [], start=1):
		item_supplier = getattr(item, "custom_consignment_supplier", None) or fallback_supplier
		if not item_supplier:
			missing_rows.append(getattr(item, "idx", index))
	return missing_rows
