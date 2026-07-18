import unittest

from client_customizations.consignment.services.reconciliation import (
	RECON_REASON_DRAFT_EXCEEDS_UNSETTLED,
	RECON_REASON_EXACT_MATCH,
	RECON_REASON_UNSETTLED_EXCEEDS_DRAFT,
	RECON_REASON_WITHIN_TOLERANCE,
	reconcile_sold_not_settled_with_draft_exposure,
)


class TestReconciliationHelpers(unittest.TestCase):
	def test_exact_match_case(self):
		result = reconcile_sold_not_settled_with_draft_exposure(
			sold_summary={"total_qty": 10, "total_amount": 200},
			settlement_exposure={
				"status_totals": {
					"Draft": {"amount": 200},
					"Submitted": {"amount": 0},
					"Cancelled": {"amount": 0},
				}
			},
		)

		self.assertEqual(result["status"], "MATCH")
		self.assertTrue(result["checks"]["amounts_match"])
		self.assertEqual(result["checks"]["delta_amount"], 0.0)
		self.assertEqual(result["indicators"][0]["code"], RECON_REASON_EXACT_MATCH)

	def test_mismatch_with_positive_and_negative_delta(self):
		positive_delta = reconcile_sold_not_settled_with_draft_exposure(
			sold_summary={"total_amount": 300},
			settlement_exposure={"status_totals": {"Draft": {"amount": 250}}},
		)
		negative_delta = reconcile_sold_not_settled_with_draft_exposure(
			sold_summary={"total_amount": 180},
			settlement_exposure={"status_totals": {"Draft": {"amount": 260}}},
		)

		self.assertEqual(positive_delta["status"], "MISMATCH")
		self.assertEqual(positive_delta["checks"]["delta_amount"], 50.0)
		self.assertEqual(positive_delta["indicators"][0]["code"], RECON_REASON_UNSETTLED_EXCEEDS_DRAFT)

		self.assertEqual(negative_delta["status"], "MISMATCH")
		self.assertEqual(negative_delta["checks"]["delta_amount"], -80.0)
		self.assertEqual(negative_delta["indicators"][0]["code"], RECON_REASON_DRAFT_EXCEEDS_UNSETTLED)

	def test_tolerance_behavior(self):
		result = reconcile_sold_not_settled_with_draft_exposure(
			sold_summary={"total_amount": 100},
			settlement_exposure={"status_totals": {"Draft": {"amount": 99.7}}},
			tolerance=0.5,
		)

		self.assertEqual(result["status"], "MATCH")
		self.assertTrue(result["checks"]["amounts_match"])
		self.assertEqual(result["indicators"][0]["code"], RECON_REASON_WITHIN_TOLERANCE)


if __name__ == "__main__":
	unittest.main()
