# Consignment Monitoring Report Functions

This slice adds service-level report functions (no UI Script Report yet) for early monitoring.

## 1) Sold Not Settled Summary (Supplier/Item/Date Scope)

```bash
bench --site <site-name> execute client_customizations.consignment.services.reporting.get_sold_not_settled_summary_by_scope --kwargs '{"company": "<company>", "posting_date_from": "2026-07-01", "posting_date_to": "2026-07-31"}'
```

Optional scope fields:

- `supplier`
- `item_code`
- `posting_date_from`
- `posting_date_to`

How to read result:

- `summary.total_qty` and `summary.total_amount`: overall unsettled sold quantity/amount in scope.
- `summary.by_supplier_item`: grouped exposure per supplier and item.
- `summary.by_posting_date`: daily exposure totals.
- `summary.skipped_count`: rows ignored because canonical minimum data was missing.

## 2) Settlement Status Exposure (Draft/Submitted/Cancelled)

```bash
bench --site <site-name> execute client_customizations.consignment.services.reporting.get_settlement_status_exposure --kwargs '{"company": "<company>", "posting_date_from": "2026-07-01", "posting_date_to": "2026-07-31"}'
```

Optional scope field:

- `supplier`

How to read result:

- `exposure.by_supplier_date`: each supplier/date bucket with per-status count and amount.
- `exposure.status_totals`: rolled-up status counts and amounts for the full scope.

Notes:

- This is intentionally service-first and bench-executable for validation.
- UI report layer can consume these payloads in a later slice.
