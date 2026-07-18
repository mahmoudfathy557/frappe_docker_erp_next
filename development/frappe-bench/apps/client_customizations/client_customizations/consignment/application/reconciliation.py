from client_customizations.consignment.application.reporting import (
	get_settlement_status_exposure,
	get_sold_not_settled_summary_by_scope,
)


RECON_REASON_EXACT_MATCH = "EXACT_MATCH"
RECON_REASON_WITHIN_TOLERANCE = "WITHIN_TOLERANCE"
RECON_REASON_NO_DRAFT_FOR_UNSETTLED = "NO_DRAFT_FOR_UNSETTLED"
RECON_REASON_DRAFT_WITHOUT_UNSETTLED = "DRAFT_WITHOUT_UNSETTLED"
RECON_REASON_UNSETTLED_EXCEEDS_DRAFT = "UNSETTLED_EXCEEDS_DRAFT"
RECON_REASON_DRAFT_EXCEEDS_UNSETTLED = "DRAFT_EXCEEDS_UNSETTLED"
RECON_REASON_SUBMITTED_EXISTS_IN_SCOPE = "SUBMITTED_EXISTS_IN_SCOPE"
RECON_REASON_CANCELLED_EXISTS_IN_SCOPE = "CANCELLED_EXISTS_IN_SCOPE"


def to_float(value):
	return float(value or 0)


def make_indicator(code, severity, message):
	return {
		"code": code,
		"severity": severity,
		"message": message,
	}


def build_reconciliation_indicators(
	sold_total_amount,
	draft_total_amount,
	delta_amount,
	absolute_delta_amount,
	tolerance,
	submitted_total_amount,
	cancelled_total_amount,
):
	"""Pure helper to reason-code reconciliation outcomes for finance operators."""
	indicators = []
	amounts_match = absolute_delta_amount <= tolerance

	if amounts_match:
		if absolute_delta_amount == 0:
			indicators.append(
				make_indicator(
					RECON_REASON_EXACT_MATCH,
					"info",
					"Sold-not-settled total amount and draft exposure are exactly aligned.",
				)
			)
		else:
			indicators.append(
				make_indicator(
					RECON_REASON_WITHIN_TOLERANCE,
					"info",
					"Difference is within configured tolerance.",
				)
			)
	else:
		if sold_total_amount > 0 and draft_total_amount == 0:
			indicators.append(
				make_indicator(
					RECON_REASON_NO_DRAFT_FOR_UNSETTLED,
					"warning",
					"Unsettled sold amount exists but no draft settlement exposure was found.",
				)
			)
		elif sold_total_amount == 0 and draft_total_amount > 0:
			indicators.append(
				make_indicator(
					RECON_REASON_DRAFT_WITHOUT_UNSETTLED,
					"warning",
					"Draft settlement exposure exists without sold-not-settled amount in scope.",
				)
			)
		elif delta_amount > 0:
			indicators.append(
				make_indicator(
					RECON_REASON_UNSETTLED_EXCEEDS_DRAFT,
					"warning",
					"Sold-not-settled amount is greater than draft settlement exposure.",
				)
			)
		else:
			indicators.append(
				make_indicator(
					RECON_REASON_DRAFT_EXCEEDS_UNSETTLED,
					"warning",
					"Draft settlement exposure is greater than sold-not-settled amount.",
				)
			)

	if submitted_total_amount > 0:
		indicators.append(
			make_indicator(
				RECON_REASON_SUBMITTED_EXISTS_IN_SCOPE,
				"info",
				"Submitted settlements also exist in scope; reconcile lifecycle timing before action.",
			)
		)
	if cancelled_total_amount > 0:
		indicators.append(
			make_indicator(
				RECON_REASON_CANCELLED_EXISTS_IN_SCOPE,
				"info",
				"Cancelled settlements exist in scope; review if cancellations affect expected exposure.",
			)
		)

	return indicators


def reconcile_sold_not_settled_with_draft_exposure(sold_summary, settlement_exposure, tolerance=0.0):
	"""Pure helper that compares sold-not-settled totals against draft settlement exposure."""
	sold_summary = sold_summary or {}
	settlement_exposure = settlement_exposure or {}
	status_totals = settlement_exposure.get("status_totals") or {}

	tolerance = max(0.0, to_float(tolerance))
	sold_total_qty = to_float(sold_summary.get("total_qty"))
	sold_total_amount = to_float(sold_summary.get("total_amount"))
	draft_total_amount = to_float((status_totals.get("Draft") or {}).get("amount"))
	submitted_total_amount = to_float((status_totals.get("Submitted") or {}).get("amount"))
	cancelled_total_amount = to_float((status_totals.get("Cancelled") or {}).get("amount"))

	delta_amount = sold_total_amount - draft_total_amount
	absolute_delta_amount = abs(delta_amount)
	amounts_match = absolute_delta_amount <= tolerance

	indicators = build_reconciliation_indicators(
		sold_total_amount=sold_total_amount,
		draft_total_amount=draft_total_amount,
		delta_amount=delta_amount,
		absolute_delta_amount=absolute_delta_amount,
		tolerance=tolerance,
		submitted_total_amount=submitted_total_amount,
		cancelled_total_amount=cancelled_total_amount,
	)

	return {
		"status": "MATCH" if amounts_match else "MISMATCH",
		"checks": {
			"amounts_match": amounts_match,
			"delta_amount": delta_amount,
			"absolute_delta_amount": absolute_delta_amount,
			"tolerance": tolerance,
		},
		"totals": {
			"sold_not_settled_qty": sold_total_qty,
			"sold_not_settled_amount": sold_total_amount,
			"draft_settlement_amount": draft_total_amount,
			"submitted_settlement_amount": submitted_total_amount,
			"cancelled_settlement_amount": cancelled_total_amount,
		},
		"indicators": indicators,
	}


def get_finance_reconciliation_by_scope(
	company,
	supplier=None,
	item_code=None,
	posting_date_from=None,
	posting_date_to=None,
	tolerance=0.0,
):
	"""Runtime wrapper for bench execute that composes existing report services."""
	sold_payload = get_sold_not_settled_summary_by_scope(
		company=company,
		supplier=supplier,
		item_code=item_code,
		posting_date_from=posting_date_from,
		posting_date_to=posting_date_to,
	)
	exposure_payload = get_settlement_status_exposure(
		company=company,
		supplier=supplier,
		posting_date_from=posting_date_from,
		posting_date_to=posting_date_to,
	)

	reconciliation = reconcile_sold_not_settled_with_draft_exposure(
		sold_summary=sold_payload.get("summary"),
		settlement_exposure=exposure_payload.get("exposure"),
		tolerance=tolerance,
	)

	return {
		"scope": {
			"company": company,
			"supplier": supplier,
			"item_code": item_code,
			"posting_date_from": posting_date_from,
			"posting_date_to": posting_date_to,
			"tolerance": max(0.0, to_float(tolerance)),
		},
		"sold_not_settled": sold_payload.get("summary"),
		"settlement_exposure": exposure_payload.get("exposure"),
		"reconciliation": reconciliation,
	}
