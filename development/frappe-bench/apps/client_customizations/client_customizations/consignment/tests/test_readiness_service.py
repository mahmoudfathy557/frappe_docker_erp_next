import unittest

from client_customizations.consignment.services.readiness import (
	STATUS_FAIL,
	STATUS_PASS,
	STATUS_WARN,
	aggregate_overall_status,
	build_readiness_payload,
	make_check_result,
)


class TestReadinessServiceHelpers(unittest.TestCase):
	def test_aggregate_overall_status_prefers_fail_over_warn_over_pass(self):
		checks = [
			{"name": "a", "status": STATUS_PASS, "details": "ok"},
			{"name": "b", "status": STATUS_WARN, "details": "warn"},
			{"name": "c", "status": STATUS_FAIL, "details": "fail"},
		]

		self.assertEqual(aggregate_overall_status(checks), STATUS_FAIL)

	def test_aggregate_overall_status_returns_pass_when_all_pass(self):
		checks = [
			{"name": "a", "status": STATUS_PASS, "details": "ok"},
			{"name": "b", "status": STATUS_PASS, "details": "ok"},
		]

		self.assertEqual(aggregate_overall_status(checks), STATUS_PASS)

	def test_make_check_result_includes_missing_items_when_provided(self):
		result = make_check_result(
			name="required_custom_fields",
			status=STATUS_FAIL,
			details="field check",
			missing_items=["A", "B"],
		)

		self.assertEqual(result["missing_items"], ["A", "B"])


class TestReadinessPayload(unittest.TestCase):
	def test_build_readiness_payload_all_pass(self):
		payload = build_readiness_payload(
			existing_doctypes=(
				"Consignment Agreement",
				"Consignment Agreement Item",
				"Consignment Settlement",
				"Consignment Settlement Item",
			),
			existing_custom_fields=(
				"Purchase Receipt-custom_is_consignment",
				"Purchase Receipt Item-custom_is_consignment",
				"Purchase Receipt Item-custom_consignment_supplier",
				"Delivery Note-custom_is_consignment",
				"Delivery Note-custom_consignment_supplier",
				"Delivery Note Item-custom_is_consignment",
				"Delivery Note Item-custom_consignment_supplier",
				"Delivery Note Item-custom_consignment_settlement",
				"Sales Invoice-custom_is_consignment",
				"Sales Invoice-custom_consignment_supplier",
				"Sales Invoice Item-custom_is_consignment",
				"Sales Invoice Item-custom_consignment_supplier",
				"Sales Invoice Item-custom_consignment_settlement",
				"Purchase Invoice-custom_consignment_settlement",
			),
			actual_doc_events={
				"Purchase Receipt": {
					"before_save": "client_customizations.consignment.validations.validate_purchase_receipt_for_consignment",
				},
				"Delivery Note": {
					"on_submit": "client_customizations.consignment.validations.validate_sale_posting_for_consignment",
					"on_cancel": "client_customizations.consignment.validations.validate_sale_cancel_not_linked_to_submitted_settlement",
				},
				"Sales Invoice": {
					"on_submit": "client_customizations.consignment.validations.validate_sale_posting_for_consignment",
					"on_cancel": "client_customizations.consignment.validations.validate_sale_cancel_not_linked_to_submitted_settlement",
				},
			},
			actual_scheduler_events={
				"daily": [
					"client_customizations.consignment.jobs.generate_daily_draft_settlements",
				]
			},
		)

		self.assertEqual(payload["overall_status"], STATUS_PASS)
		self.assertEqual(len(payload["checks"]), 4)
		self.assertTrue(all(check["status"] == STATUS_PASS for check in payload["checks"]))

	def test_build_readiness_payload_reports_missing_items_and_fails(self):
		payload = build_readiness_payload(
			existing_doctypes=("Consignment Agreement",),
			existing_custom_fields=("Purchase Receipt-custom_is_consignment",),
			actual_doc_events={
				"Purchase Receipt": {
					"before_save": "client_customizations.consignment.validations.validate_purchase_receipt_for_consignment",
				},
			},
			actual_scheduler_events={},
		)

		self.assertEqual(payload["overall_status"], STATUS_FAIL)

		check_map = {check["name"]: check for check in payload["checks"]}
		self.assertGreater(len(check_map["required_doctypes"]["missing_items"]), 0)
		self.assertGreater(len(check_map["required_custom_fields"]["missing_items"]), 0)
		self.assertGreater(len(check_map["doc_event_hooks"]["missing_items"]), 0)
		self.assertGreater(len(check_map["scheduler_hooks"]["missing_items"]), 0)


if __name__ == "__main__":
	unittest.main()
