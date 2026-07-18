import unittest

from client_customizations.consignment.jobs import (
	_select_target_company_names,
	build_company_summary,
)


class TestJobHelpers(unittest.TestCase):
	def test_selects_all_companies_for_scheduler_default(self):
		companies = [{"name": "Company A"}, {"name": "Company B"}, {"ignored": "x"}]

		result = _select_target_company_names(companies)

		self.assertEqual(result, ["Company A", "Company B"])

	def test_selects_only_requested_company_for_manual_execution(self):
		companies = [{"name": "Company A"}, {"name": "Company B"}]

		result = _select_target_company_names(companies, company="Company B")

		self.assertEqual(result, ["Company B"])

	def test_builds_compact_company_summary_payload(self):
		result = build_company_summary("Company A", created_count=3, skipped_count=2)

		self.assertEqual(
			result,
			{
				"company": "Company A",
				"created_count": 3,
				"skipped_count": 2,
			},
		)


if __name__ == "__main__":
	unittest.main()
