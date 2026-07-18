import unittest

from client_customizations.consignment.services.payable import (
	build_purchase_invoice_items_from_settlement_items,
	build_purchase_invoice_payload_from_settlement,
	payable_status_from_docstatus,
	should_block_settlement_cancel_for_payable_docstatus,
	should_create_payable_for_settlement,
)


class TestPayableServiceHelpers(unittest.TestCase):
	def test_payable_status_mapping(self):
		self.assertEqual(payable_status_from_docstatus(0), "Draft")
		self.assertEqual(payable_status_from_docstatus(1), "Submitted")
		self.assertEqual(payable_status_from_docstatus(2), "Cancelled")
		self.assertEqual(payable_status_from_docstatus(None), "Not Generated")

	def test_idempotency_helper_for_creation_decision(self):
		self.assertTrue(should_create_payable_for_settlement("", None))
		self.assertFalse(should_create_payable_for_settlement("PINV-0001", None))
		self.assertFalse(should_create_payable_for_settlement("", {"name": "PINV-0002", "docstatus": 0}))

	def test_cancel_policy_helper_blocks_only_submitted_payables(self):
		self.assertFalse(should_block_settlement_cancel_for_payable_docstatus(0))
		self.assertTrue(should_block_settlement_cancel_for_payable_docstatus(1))
		self.assertFalse(should_block_settlement_cancel_for_payable_docstatus(2))

	def test_builds_purchase_invoice_items_from_settlement_rows(self):
		rows = [
			{
				"sales_doctype": "Sales Invoice",
				"sales_document": "SINV-0001",
				"sales_row": "SII-0001",
				"item_code": "ITEM-001",
				"qty": 2,
				"base_amount": 100,
			},
			{
				"sales_doctype": "Delivery Note",
				"sales_document": "DN-0001",
				"sales_row": "DNI-0001",
				"item_code": "ITEM-002",
				"qty": 3,
				"base_amount": 90,
			},
		]

		items = build_purchase_invoice_items_from_settlement_items(rows)

		self.assertEqual(len(items), 2)
		self.assertEqual(items[0]["item_code"], "ITEM-001")
		self.assertEqual(items[0]["qty"], 2.0)
		self.assertEqual(items[0]["rate"], 50.0)
		self.assertEqual(items[1]["rate"], 30.0)
		self.assertIn("Consignment settlement source", items[0]["description"])

	def test_builds_purchase_invoice_payload_from_settlement(self):
		settlement = {
			"name": "CST-0001",
			"company": "Test Company",
			"supplier": "Supp-A",
			"posting_date": "2026-07-18",
			"items": [
				{
					"sales_doctype": "Sales Invoice",
					"sales_document": "SINV-0099",
					"sales_row": "SII-0099",
					"item_code": "ITEM-0099",
					"qty": 4,
					"base_amount": 200,
				}
			],
		}

		payload = build_purchase_invoice_payload_from_settlement(settlement)

		self.assertEqual(payload["doctype"], "Purchase Invoice")
		self.assertEqual(payload["company"], "Test Company")
		self.assertEqual(payload["supplier"], "Supp-A")
		self.assertEqual(payload["custom_consignment_settlement"], "CST-0001")
		self.assertEqual(payload["items"][0]["rate"], 50.0)
		self.assertIn("CST-0001", payload["remarks"])


if __name__ == "__main__":
	unittest.main()
