import unittest

from client_customizations.consignment.services.settlement import (
	aggregate_sold_not_settled_rows,
	aggregate_skip_reasons,
	build_draft_settlement_lines,
	classify_row_skip_reason,
	compute_totals_from_lines,
	group_rows_by_supplier_item,
	normalize_settlement_row,
	partition_settlement_rows_with_reasons,
	should_clear_source_row_link,
	should_create_draft_for_supplier,
	split_grouped_lines_by_supplier,
)


class TestSettlementAggregation(unittest.TestCase):
	def test_aggregates_only_unsettled_rows(self):
		rows = [
			{
				"item_code": "ITEM-001",
				"qty": 2,
				"base_net_amount": 150,
				"custom_consignment_settlement": "",
			},
			{
				"item_code": "ITEM-001",
				"qty": 1,
				"base_net_amount": 75,
				"custom_consignment_settlement": "SETTLE-0001",
			},
			{
				"item_code": "ITEM-002",
				"qty": 3,
				"base_net_amount": 210,
				"custom_consignment_settlement": None,
			},
		]

		result = aggregate_sold_not_settled_rows(rows)

		self.assertEqual(result["total_qty"], 5.0)
		self.assertEqual(result["total_amount"], 360.0)
		self.assertEqual(result["by_item"]["ITEM-001"]["qty"], 2.0)
		self.assertEqual(result["by_item"]["ITEM-002"]["amount"], 210.0)

	def test_builds_draft_settlement_lines_grouped_by_supplier_and_item(self):
		rows = [
			{
				"name": "SII-0001",
				"parent": "SINV-0001",
				"sales_doctype": "Sales Invoice",
				"item_code": "ITEM-001",
				"qty": 2,
				"base_net_amount": 100,
				"custom_consignment_supplier": "SUP-A",
				"custom_consignment_settlement": "",
			},
			{
				"name": "SII-0002",
				"parent": "SINV-0002",
				"sales_doctype": "Sales Invoice",
				"item_code": "ITEM-001",
				"qty": 3,
				"base_net_amount": 150,
				"custom_consignment_supplier": "SUP-A",
				"custom_consignment_settlement": None,
			},
			{
				"name": "SII-0003",
				"parent": "SINV-0003",
				"sales_doctype": "Sales Invoice",
				"item_code": "ITEM-002",
				"qty": 1,
				"base_net_amount": 80,
				"custom_consignment_supplier": "SUP-B",
				"custom_consignment_settlement": "CS-0001",
			},
		]

		result = build_draft_settlement_lines(rows)

		self.assertEqual(len(result), 1)
		self.assertEqual(result[0]["supplier"], "SUP-A")
		self.assertEqual(result[0]["item_code"], "ITEM-001")
		self.assertEqual(result[0]["qty"], 5.0)
		self.assertEqual(result[0]["base_amount"], 250.0)
		self.assertEqual(len(result[0]["source_rows"]), 2)

	def test_groups_normalized_rows_by_supplier_and_item(self):
		rows = [
			{
				"sales_doctype": "Sales Invoice",
				"sales_document": "SINV-0001",
				"sales_row": "SII-0001",
				"supplier": "SUP-A",
				"item_code": "ITEM-001",
				"qty": 2,
				"base_amount": 120,
			},
			{
				"sales_doctype": "Delivery Note",
				"sales_document": "DN-0001",
				"sales_row": "DNI-0001",
				"supplier": "SUP-A",
				"item_code": "ITEM-001",
				"qty": 1,
				"base_amount": 60,
			},
			{
				"sales_doctype": "Sales Invoice",
				"sales_document": "SINV-0002",
				"sales_row": "SII-0002",
				"supplier": "SUP-B",
				"item_code": "ITEM-002",
				"qty": 4,
				"base_amount": 200,
			},
		]

		grouped = group_rows_by_supplier_item(rows)
		by_key = {(row["supplier"], row["item_code"]): row for row in grouped}

		self.assertEqual(len(grouped), 2)
		self.assertEqual(by_key[("SUP-A", "ITEM-001")]["qty"], 3.0)
		self.assertEqual(by_key[("SUP-A", "ITEM-001")]["base_amount"], 180.0)
		self.assertEqual(len(by_key[("SUP-A", "ITEM-001")]["source_rows"]), 2)

	def test_splits_grouped_lines_by_supplier_bucket(self):
		grouped_lines = [
			{"supplier": "SUP-A", "item_code": "ITEM-001", "qty": 3, "base_amount": 180, "source_rows": []},
			{"supplier": "SUP-A", "item_code": "ITEM-002", "qty": 1, "base_amount": 40, "source_rows": []},
			{"supplier": "SUP-B", "item_code": "ITEM-001", "qty": 2, "base_amount": 90, "source_rows": []},
		]

		buckets = split_grouped_lines_by_supplier(grouped_lines)

		self.assertEqual(sorted(buckets.keys()), ["SUP-A", "SUP-B"])
		self.assertEqual(len(buckets["SUP-A"]), 2)
		self.assertEqual(len(buckets["SUP-B"]), 1)

	def test_computes_totals_from_lines(self):
		lines = [
			{"qty": 2, "base_amount": 50},
			{"qty": 3, "base_amount": 90},
		]

		result = compute_totals_from_lines(lines)

		self.assertEqual(result["total_qty"], 5.0)
		self.assertEqual(result["total_amount"], 140.0)

	def test_idempotency_helper_for_supplier_posting_date(self):
		existing = {("SUP-A", "2026-07-18")}

		self.assertFalse(should_create_draft_for_supplier("SUP-A", "2026-07-18", existing))
		self.assertTrue(should_create_draft_for_supplier("SUP-A", "2026-07-19", existing))
		self.assertTrue(should_create_draft_for_supplier("SUP-B", "2026-07-18", existing))

	def test_normalizes_rows_to_canonical_schema(self):
		row = {
			"doctype": "Sales Invoice",
			"parent": "SINV-0001",
			"name": "SII-0001",
			"custom_consignment_supplier": "SUP-A",
			"item_code": "ITEM-001",
			"qty": 2,
			"base_net_amount": 100,
			"custom_consignment_settlement": "",
		}

		result = normalize_settlement_row(row)

		self.assertEqual(result["sales_doctype"], "Sales Invoice")
		self.assertEqual(result["sales_document"], "SINV-0001")
		self.assertEqual(result["sales_row"], "SII-0001")
		self.assertEqual(result["supplier"], "SUP-A")
		self.assertEqual(result["qty"], 2.0)
		self.assertEqual(result["base_amount"], 100.0)

	def test_build_lines_keeps_public_behavior_with_canonical_path(self):
		rows = [
			{
				"doctype": "Sales Invoice",
				"parent": "SINV-0101",
				"name": "SII-0101",
				"custom_consignment_supplier": "SUP-A",
				"item_code": "ITEM-100",
				"qty": 1,
				"base_net_amount": 20,
				"custom_consignment_settlement": None,
			},
			{
				"doctype": "Delivery Note",
				"parent": "DN-0101",
				"name": "DNI-0101",
				"custom_consignment_supplier": "SUP-A",
				"item_code": "ITEM-100",
				"qty": 2,
				"base_amount": 55,
				"custom_consignment_settlement": "",
			},
		]

		result = build_draft_settlement_lines(rows)

		self.assertEqual(len(result), 1)
		self.assertEqual(result[0]["supplier"], "SUP-A")
		self.assertEqual(result[0]["item_code"], "ITEM-100")
		self.assertEqual(result[0]["qty"], 3.0)
		self.assertEqual(result[0]["base_amount"], 75.0)
		self.assertEqual(len(result[0]["source_rows"]), 2)

	def test_classifies_skip_reasons_from_canonical_rows(self):
		self.assertEqual(
			classify_row_skip_reason(
				{
					"sales_doctype": "Sales Invoice",
					"sales_document": "SINV-0010",
					"sales_row": "SII-0010",
					"supplier": None,
					"item_code": "ITEM-1",
					"custom_consignment_settlement": "",
				}
			),
			"MISSING_SUPPLIER",
		)
		self.assertEqual(
			classify_row_skip_reason(
				{
					"sales_doctype": "Delivery Note",
					"sales_document": "DN-0010",
					"sales_row": "DNI-0010",
					"supplier": "SUP-A",
					"item_code": None,
					"custom_consignment_settlement": "",
				}
			),
			"MISSING_ITEM",
		)
		self.assertEqual(
			classify_row_skip_reason(
				{
					"sales_doctype": "Delivery Note",
					"sales_document": "DN-0011",
					"sales_row": "DNI-0011",
					"supplier": "SUP-A",
					"item_code": "ITEM-2",
					"custom_consignment_settlement": "CST-0001",
				}
			),
			"ALREADY_SETTLED",
		)

	def test_partitions_rows_and_aggregates_reason_counts(self):
		rows = [
			{
				"doctype": "Sales Invoice",
				"parent": "SINV-1001",
				"name": "SII-1001",
				"custom_consignment_supplier": "SUP-A",
				"item_code": "ITEM-1",
				"qty": 1,
				"base_net_amount": 50,
				"custom_consignment_settlement": "",
			},
			{
				"doctype": "Sales Invoice",
				"parent": "SINV-1002",
				"name": "SII-1002",
				"item_code": "ITEM-1",
				"qty": 1,
				"base_net_amount": 60,
				"custom_consignment_settlement": "",
			},
			{
				"doctype": "Delivery Note",
				"parent": "DN-1003",
				"name": "DNI-1003",
				"custom_consignment_supplier": "SUP-C",
				"qty": 1,
				"base_amount": 70,
				"custom_consignment_settlement": "",
			},
			{
				"doctype": "Delivery Note",
				"parent": "DN-1004",
				"name": "DNI-1004",
				"custom_consignment_supplier": "SUP-C",
				"item_code": "ITEM-2",
				"qty": 1,
				"base_amount": 70,
				"custom_consignment_settlement": "CST-0009",
			},
		]

		accepted, skipped = partition_settlement_rows_with_reasons(rows)

		self.assertEqual(len(accepted), 1)
		self.assertEqual(len(skipped), 3)
		self.assertEqual(
			aggregate_skip_reasons(skipped),
			{
				"MISSING_SUPPLIER": 1,
				"MISSING_ITEM": 1,
				"ALREADY_SETTLED": 1,
			},
		)

	def test_clear_link_helper_is_idempotent_and_strict(self):
		self.assertTrue(should_clear_source_row_link("CST-0001", "CST-0001"))
		self.assertFalse(should_clear_source_row_link("CST-0002", "CST-0001"))
		self.assertFalse(should_clear_source_row_link("", "CST-0001"))


if __name__ == "__main__":
	unittest.main()
