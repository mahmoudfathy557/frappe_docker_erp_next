import frappe
from frappe.model.document import Document

from client_customizations.consignment.application.payable import (
	enforce_settlement_cancel_payable_policy,
	ensure_payable_for_submitted_settlement,
)
from client_customizations.consignment.application.settlement import clear_source_rows_settlement_link


class ConsignmentSettlement(Document):
	VALID_STATUSES = {"Draft", "Ready to Submit", "Submitted", "Cancelled"}

	def before_save(self):
		self._normalize_status_v1()
		self._compute_totals()

	def validate(self):
		if not self.items:
			frappe.throw("Consignment Settlement requires at least one item row")

		if not self.supplier:
			frappe.throw("Supplier is required on Consignment Settlement header")

		for row in self.items:
			if not row.supplier:
				frappe.throw(f"Row #{row.idx}: supplier is required")
			if row.supplier != self.supplier:
				frappe.throw(
					f"Row #{row.idx}: supplier {row.supplier} must match header supplier {self.supplier}"
				)
			if not row.item_code:
				frappe.throw(f"Row #{row.idx}: item_code is required")
			if row.qty in (None, ""):
				frappe.throw(f"Row #{row.idx}: qty is required")
			if float(row.qty or 0) <= 0:
				frappe.throw(f"Row #{row.idx}: qty must be greater than 0")
			if float(row.base_amount or 0) < 0:
				frappe.throw(f"Row #{row.idx}: base_amount cannot be negative")

		self._normalize_status_v1()

	def on_cancel(self):
		"""Apply payable policy and reverse source-row links for this settlement."""
		enforce_settlement_cancel_payable_policy(self)
		clear_source_rows_settlement_link(items=self.items, settlement_name=self.name)

	def on_submit(self):
		ensure_payable_for_submitted_settlement(self)

	def _compute_totals(self):
		total_qty = 0.0
		total_amount = 0.0
		for row in self.items or []:
			total_qty += float(row.qty or 0)
			total_amount += float(row.base_amount or 0)

		self.total_qty = total_qty
		self.total_amount = total_amount

	def _normalize_status_v1(self):
		if self.docstatus == 2:
			self.status = "Cancelled"
		elif self.docstatus == 1:
			self.status = "Submitted"
		elif not self.status or self.status in {"Submitted", "Cancelled"}:
			self.status = "Draft"

		if self.status not in self.VALID_STATUSES:
			frappe.throw("Invalid status for Consignment Settlement")
