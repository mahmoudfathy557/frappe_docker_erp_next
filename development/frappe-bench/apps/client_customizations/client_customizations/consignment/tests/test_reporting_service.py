import unittest

from client_customizations.consignment.services.reporting import (
	build_settlement_status_exposure_dataset,
	build_sold_not_settled_dataset,
	bucket_numeric_rows,
	make_scope_filters,
)


class TestReportingServiceHelpers(unittest.TestCase):
	def test_builds_scope_filters_for_open_and_closed_date_ranges(self):
		self.assertEqual(
			make_scope_filters("My Co", posting_date_from="2026-07-01", posting_date_to="2026-07-31"),
			{
				"docstatus": 1,
				"company": "My Co",
				"custom_is_consignment": 1,
				"posting_date": ["between", ["2026-07-01", "2026-07-31"]],
			},
		)
		self.assertEqual(
			make_scope_filters("My Co", supplier="SUP-1", posting_date_from="2026-07-01"),
			{
				"docstatus": 1,
				"company": "My Co",
				"custom_is_consignment": 1,
				"custom_consignment_supplier": "SUP-1",
				"posting_date": [">=", "2026-07-01"],
			},
		)

	def test_buckets_numeric_rows_by_group_fields(self):
		rows = [
			{"supplier": "SUP-A", "item_code": "ITEM-1", "qty": 2, "base_amount": 40},
			{"supplier": "SUP-A", "item_code": "ITEM-1", "qty": 1, "base_amount": 20},
			{"supplier": "SUP-B", "item_code": "ITEM-1", "qty": 5, "base_amount": 90},
		]

		result = bucket_numeric_rows(rows, ["supplier", "item_code"])

		self.assertEqual(
			result,
			[
				{
					"supplier": "SUP-A",
					"item_code": "ITEM-1",
					"row_count": 2,
					"qty": 3.0,
					"amount": 60.0,
				},
				{
					"supplier": "SUP-B",
					"item_code": "ITEM-1",
					"row_count": 1,
					"qty": 5.0,
					"amount": 90.0,
				},
			],
		)

	def test_builds_sold_not_settled_dataset(self):
		rows = [
			{
				"supplier": "SUP-A",
				"item_code": "ITEM-1",
				"posting_date": "2026-07-15",
				"qty": 2,
				"base_amount": 40,
			},
			{
				"supplier": "SUP-A",
				"item_code": "ITEM-2",
				"posting_date": "2026-07-15",
				"qty": 1,
				"base_amount": 30,
			},
			{
				"supplier": "SUP-B",
				"item_code": "ITEM-1",
				"posting_date": "2026-07-16",
				"qty": 4,
				"base_amount": 100,
			},
		]

		result = build_sold_not_settled_dataset(rows, skipped_rows=[{"reason_code": "MISSING_SUPPLIER"}])

		self.assertEqual(result["total_qty"], 7.0)
		self.assertEqual(result["total_amount"], 170.0)
		self.assertEqual(result["row_count"], 3)
		self.assertEqual(result["skipped_count"], 1)
		self.assertEqual(len(result["by_supplier_item"]), 3)
		self.assertEqual(
			result["by_posting_date"],
			[
				{"posting_date": "2026-07-15", "row_count": 2, "qty": 3.0, "amount": 70.0},
				{"posting_date": "2026-07-16", "row_count": 1, "qty": 4.0, "amount": 100.0},
			],
		)

	def test_builds_settlement_status_exposure_dataset(self):
		rows = [
			{"supplier": "SUP-A", "posting_date": "2026-07-15", "status": "Draft", "total_amount": 100},
			{
				"supplier": "SUP-A",
				"posting_date": "2026-07-15",
				"status": "Submitted",
				"total_amount": 120,
			},
			{
				"supplier": "SUP-A",
				"posting_date": "2026-07-15",
				"status": "Cancelled",
				"total_amount": 10,
			},
			{
				"supplier": "SUP-B",
				"posting_date": "2026-07-16",
				"status": "Submitted",
				"total_amount": 60,
			},
			{
				"supplier": "SUP-B",
				"posting_date": "2026-07-16",
				"status": "Ready to Submit",
				"total_amount": 999,
			},
		]

		result = build_settlement_status_exposure_dataset(rows)

		self.assertEqual(len(result["by_supplier_date"]), 2)
		self.assertEqual(
			result["by_supplier_date"][0],
			{
				"supplier": "SUP-A",
				"posting_date": "2026-07-15",
				"counts": {"Draft": 1, "Submitted": 1, "Cancelled": 1},
				"amounts": {"Draft": 100.0, "Submitted": 120.0, "Cancelled": 10.0},
			},
		)
		self.assertEqual(result["status_totals"]["Draft"]["count"], 1)
		self.assertEqual(result["status_totals"]["Submitted"]["count"], 2)
		self.assertEqual(result["status_totals"]["Submitted"]["amount"], 180.0)
		self.assertEqual(result["status_totals"]["Cancelled"]["count"], 1)


if __name__ == "__main__":
	unittest.main()
