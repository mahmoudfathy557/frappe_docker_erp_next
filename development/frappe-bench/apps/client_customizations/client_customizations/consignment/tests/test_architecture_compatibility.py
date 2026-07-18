import unittest

from client_customizations.consignment.application.settlement import (
	build_draft_settlement_lines as build_lines_application,
)
from client_customizations.consignment.jobs import (
	build_company_summary as build_company_summary_compat,
)
from client_customizations.consignment.interface.jobs import (
	build_company_summary as build_company_summary_interface,
)
from client_customizations.consignment.services.settlement import (
	build_draft_settlement_lines as build_lines_compat,
)
from client_customizations.consignment.validations import (
	get_items_missing_warehouse as get_missing_warehouse_compat,
)
from client_customizations.consignment.interface.validations import (
	get_items_missing_warehouse as get_missing_warehouse_interface,
)


class TestArchitectureCompatibility(unittest.TestCase):
	def test_legacy_services_wrapper_matches_application_results(self):
		rows = [
			{
				"doctype": "Sales Invoice",
				"parent": "SINV-0001",
				"name": "SII-0001",
				"custom_consignment_supplier": "SUP-A",
				"item_code": "ITEM-1",
				"qty": 2,
				"base_net_amount": 100,
				"custom_consignment_settlement": "",
			}
		]

		self.assertEqual(build_lines_compat(rows), build_lines_application(rows))

	def test_legacy_jobs_wrapper_matches_interface_results(self):
		self.assertEqual(
			build_company_summary_compat("Company A", 2, 1),
			build_company_summary_interface("Company A", 2, 1),
		)

	def test_legacy_validations_wrapper_matches_interface_results(self):
		class _Row:
			def __init__(self, idx, warehouse):
				self.idx = idx
				self.warehouse = warehouse

		rows = [_Row(1, "Main"), _Row(2, "")]
		self.assertEqual(get_missing_warehouse_compat(rows), get_missing_warehouse_interface(rows))


if __name__ == "__main__":
	unittest.main()
