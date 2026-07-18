import unittest
from types import SimpleNamespace

from client_customizations.consignment.validations import (
	get_submitted_settlement_names,
	get_items_missing_warehouse,
	get_rows_missing_supplier_link,
	get_sales_doc_child_doctype,
	has_sale_items,
	is_consignment_doc,
)


class TestValidationHelpers(unittest.TestCase):
	def test_detects_consignment_marker(self):
		doc = SimpleNamespace(custom_is_consignment=1)
		self.assertTrue(is_consignment_doc(doc))

	def test_requires_sale_items(self):
		self.assertFalse(has_sale_items([]))
		self.assertTrue(has_sale_items([SimpleNamespace()]))

	def test_collects_rows_missing_warehouse(self):
		items = [
			SimpleNamespace(idx=1, warehouse="Main - WH"),
			SimpleNamespace(idx=2, warehouse=None),
			SimpleNamespace(idx=3, warehouse=""),
		]
		self.assertEqual(get_items_missing_warehouse(items), [2, 3])

	def test_collects_rows_missing_supplier_link_with_fallback(self):
		items = [
			SimpleNamespace(idx=1, custom_consignment_supplier="SUP-1"),
			SimpleNamespace(idx=2, custom_consignment_supplier=None),
		]
		self.assertEqual(get_rows_missing_supplier_link(items, fallback_supplier="SUP-H"), [])
		self.assertEqual(get_rows_missing_supplier_link(items, fallback_supplier=None), [2])

	def test_maps_sales_doctype_to_child_doctype(self):
		self.assertEqual(get_sales_doc_child_doctype("Sales Invoice"), "Sales Invoice Item")
		self.assertEqual(get_sales_doc_child_doctype("Delivery Note"), "Delivery Note Item")

	def test_filters_submitted_settlement_names_for_cancel_guard(self):
		state_rows = [
			{"name": "CST-0001", "docstatus": 1, "status": "Submitted"},
			{"name": "CST-0002", "docstatus": 0, "status": "Draft"},
			{"name": "CST-0003", "docstatus": 0, "status": "Submitted"},
			{"name": "CST-0001", "docstatus": 1, "status": "Submitted"},
		]
		self.assertEqual(get_submitted_settlement_names(state_rows), ["CST-0001", "CST-0003"])


if __name__ == "__main__":
	unittest.main()
