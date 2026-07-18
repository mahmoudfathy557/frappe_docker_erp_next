# Consignment Reconciliation For Finance

This command compares sold-not-settled exposure against draft settlement exposure for a scope.

## Run Command

```bash
bench --site <site-name> execute client_customizations.consignment.services.reconciliation.get_finance_reconciliation_by_scope --kwargs '{"company": "<company>", "posting_date_from": "2026-07-01", "posting_date_to": "2026-07-31", "tolerance": 0.0}'
```

Optional scope filters:

- `supplier`
- `item_code`
- `posting_date_from`
- `posting_date_to`
- `tolerance` (amount tolerance for matching, defaults to `0.0`)

## How To Interpret Result

Primary fields:

- `reconciliation.status`: `MATCH` or `MISMATCH`
- `reconciliation.checks.delta_amount`: sold-not-settled amount minus draft settlement amount
- `reconciliation.checks.absolute_delta_amount`: absolute difference used for tolerance checks
- `reconciliation.totals.sold_not_settled_amount`: exposure from sales side
- `reconciliation.totals.draft_settlement_amount`: exposure in draft settlements

Reason-coded indicators in `reconciliation.indicators` help explain mismatch context:

- `NO_DRAFT_FOR_UNSETTLED`: sales exposure exists but no draft settlements found
- `DRAFT_WITHOUT_UNSETTLED`: draft settlement amount exists without sales exposure
- `UNSETTLED_EXCEEDS_DRAFT`: sales exposure is higher than draft amount
- `DRAFT_EXCEEDS_UNSETTLED`: draft amount is higher than sales exposure
- `WITHIN_TOLERANCE`: difference exists but is accepted by tolerance

Operational note:

- Treat `MATCH` with non-zero submitted/cancelled indicators as lifecycle timing context, not a strict error.
