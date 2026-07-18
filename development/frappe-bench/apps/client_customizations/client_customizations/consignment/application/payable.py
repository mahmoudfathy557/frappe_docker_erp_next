from client_customizations.consignment.infrastructure.frappe_adapter import (
	db_get_value,
	db_set_value,
	get_doc,
	get_list,
	throw,
)


def payable_status_from_docstatus(docstatus):
	"""Pure helper to map Purchase Invoice docstatus into settlement payable status."""
	mapping = {
		0: "Draft",
		1: "Submitted",
		2: "Cancelled",
	}
	return mapping.get(docstatus, "Not Generated")


def should_create_payable_for_settlement(linked_purchase_invoice, existing_marked_purchase_invoice):
	"""Pure idempotency helper for payable creation decision."""
	return not linked_purchase_invoice and not existing_marked_purchase_invoice


def should_block_settlement_cancel_for_payable_docstatus(docstatus):
	"""Pure policy helper for safe settlement cancellation behavior."""
	return int(docstatus or 0) == 1


def _compute_item_rate(qty, base_amount):
	qty_value = float(qty or 0)
	amount_value = float(base_amount or 0)
	if qty_value <= 0:
		return 0.0
	return amount_value / qty_value


def build_purchase_invoice_items_from_settlement_items(settlement_items):
	"""Pure helper to transform settlement items into Purchase Invoice item payload."""
	items = []
	for row in settlement_items or []:
		qty = float(row.get("qty") or 0)
		amount = float(row.get("base_amount") or 0)
		items.append(
			{
				"item_code": row.get("item_code"),
				"qty": qty,
				"rate": _compute_item_rate(qty, amount),
				"amount": amount,
				"description": (
					f"Consignment settlement source {row.get('sales_doctype')} {row.get('sales_document')} "
					f"row {row.get('sales_row')}"
				),
			}
		)
	return items


def build_purchase_invoice_payload_from_settlement(settlement_doc):
	"""Pure helper to build deterministic draft Purchase Invoice payload from settlement."""
	settlement_name = settlement_doc.get("name")
	items = build_purchase_invoice_items_from_settlement_items(settlement_doc.get("items"))
	return {
		"doctype": "Purchase Invoice",
		"company": settlement_doc.get("company"),
		"supplier": settlement_doc.get("supplier"),
		"posting_date": settlement_doc.get("posting_date"),
		"custom_consignment_settlement": settlement_name,
		"remarks": f"Generated from Consignment Settlement {settlement_name}",
		"items": items,
	}


def _get_existing_purchase_invoice_by_settlement_marker(settlement_name):
	rows = get_list(
		"Purchase Invoice",
		fields=["name", "docstatus"],
		filters={"custom_consignment_settlement": settlement_name},
		order_by="creation desc",
		limit_page_length=1,
	)
	return rows[0] if rows else None


def _set_settlement_payable_link_state(settlement_name, purchase_invoice_name, purchase_invoice_docstatus):
	db_set_value("Consignment Settlement", settlement_name, "linked_purchase_invoice", purchase_invoice_name or "")
	db_set_value(
		"Consignment Settlement",
		settlement_name,
		"payable_status",
		payable_status_from_docstatus(purchase_invoice_docstatus),
	)


def ensure_payable_for_submitted_settlement(settlement_doc):
	"""Ensure one draft Purchase Invoice exists per submitted settlement (idempotent)."""
	linked_purchase_invoice = settlement_doc.get("linked_purchase_invoice")
	if linked_purchase_invoice:
		linked_docstatus = db_get_value("Purchase Invoice", linked_purchase_invoice, "docstatus")
		if linked_docstatus is not None:
			_set_settlement_payable_link_state(
				settlement_name=settlement_doc.get("name"),
				purchase_invoice_name=linked_purchase_invoice,
				purchase_invoice_docstatus=linked_docstatus,
			)
			return {"status": "already-linked", "purchase_invoice": linked_purchase_invoice}

	existing_marker_row = _get_existing_purchase_invoice_by_settlement_marker(settlement_doc.get("name"))
	if not should_create_payable_for_settlement(linked_purchase_invoice, existing_marker_row):
		_set_settlement_payable_link_state(
			settlement_name=settlement_doc.get("name"),
			purchase_invoice_name=existing_marker_row.get("name") if existing_marker_row else linked_purchase_invoice,
			purchase_invoice_docstatus=existing_marker_row.get("docstatus") if existing_marker_row else 0,
		)
		return {
			"status": "found-existing-marker",
			"purchase_invoice": existing_marker_row.get("name") if existing_marker_row else linked_purchase_invoice,
		}

	payload = build_purchase_invoice_payload_from_settlement(settlement_doc)
	purchase_invoice = get_doc(payload)
	purchase_invoice.insert(ignore_permissions=True)

	_set_settlement_payable_link_state(
		settlement_name=settlement_doc.get("name"),
		purchase_invoice_name=purchase_invoice.name,
		purchase_invoice_docstatus=purchase_invoice.docstatus,
	)

	return {"status": "created", "purchase_invoice": purchase_invoice.name}


def enforce_settlement_cancel_payable_policy(settlement_doc):
	"""Safe v1 cancel policy.

	- Block settlement cancel if linked PI is submitted.
	- Delete linked PI if it is draft.
	- Keep link/status if linked PI is already cancelled.
	"""
	linked_purchase_invoice = settlement_doc.get("linked_purchase_invoice")
	if not linked_purchase_invoice:
		return {"status": "no-payable"}

	purchase_invoice_docstatus = db_get_value("Purchase Invoice", linked_purchase_invoice, "docstatus")
	if purchase_invoice_docstatus is None:
		_set_settlement_payable_link_state(
			settlement_name=settlement_doc.get("name"),
			purchase_invoice_name="",
			purchase_invoice_docstatus=None,
		)
		return {"status": "missing-payable-cleared"}

	if should_block_settlement_cancel_for_payable_docstatus(purchase_invoice_docstatus):
		throw(
			f"Cannot cancel Consignment Settlement {settlement_doc.get('name')} because linked Purchase Invoice "
			f"{linked_purchase_invoice} is submitted. Cancel the Purchase Invoice first."
		)

	if int(purchase_invoice_docstatus) == 0:
		purchase_invoice = get_doc("Purchase Invoice", linked_purchase_invoice)
		purchase_invoice.delete(ignore_permissions=True)
		_set_settlement_payable_link_state(
			settlement_name=settlement_doc.get("name"),
			purchase_invoice_name="",
			purchase_invoice_docstatus=None,
		)
		return {"status": "draft-payable-deleted"}

	_set_settlement_payable_link_state(
		settlement_name=settlement_doc.get("name"),
		purchase_invoice_name=linked_purchase_invoice,
		purchase_invoice_docstatus=purchase_invoice_docstatus,
	)
	return {"status": "cancelled-payable-linked"}
