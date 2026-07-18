from datetime import date

from client_customizations.consignment.application.settlement import generate_draft_settlements_for_date
from client_customizations.consignment.infrastructure.frappe_adapter import get_list


def _select_target_company_names(companies, company=None):
	"""Pure helper to select scheduler target companies with optional manual company filter."""
	company_names = [row.get("name") for row in (companies or []) if row.get("name")]
	if company:
		return [name for name in company_names if name == company]
	return company_names


def build_company_summary(company, created_count, skipped_count):
	"""Pure helper to return compact scheduler summary payload."""
	return {
		"company": company,
		"created_count": int(created_count or 0),
		"skipped_count": int(skipped_count or 0),
	}


def generate_daily_draft_settlements(posting_date=None, dry_run=False, company=None):
	"""Scheduler entrypoint: generate draft settlements per company for one posting date."""
	target_posting_date = posting_date or date.today().isoformat()
	companies = get_list("Company", fields=["name"], filters={}, limit_page_length=0)
	target_company_names = _select_target_company_names(companies, company=company)

	results = []
	for company_name in target_company_names:
		company_result = generate_draft_settlements_for_date(
			company=company_name,
			posting_date=target_posting_date,
			dry_run=dry_run,
			include_summary=True,
		)
		results.append(
			build_company_summary(
				company=company_name,
				created_count=company_result.get("created_count", 0),
				skipped_count=company_result.get("skipped_count", 0),
			)
		)

	return results
