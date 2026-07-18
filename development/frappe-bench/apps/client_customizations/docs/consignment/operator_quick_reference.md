# Consignment Operator Quick Reference

Use this page during daily finance operations.

## 1. Daily Commands

Preview reason-coded summary for one company/date:

```bash
bench --site <site-name> execute client_customizations.consignment.services.settlement.generate_draft_settlements_for_date --kwargs '{"company": "<company-name>", "posting_date": "<yyyy-mm-dd>", "dry_run": true, "include_summary": true}'
```

Run settlement generation for all companies/date:

```bash
bench --site <site-name> execute client_customizations.consignment.jobs.generate_daily_draft_settlements --kwargs '{"posting_date": "<yyyy-mm-dd>"}'
```

Run settlement generation for one company/date:

```bash
bench --site <site-name> execute client_customizations.consignment.jobs.generate_daily_draft_settlements --kwargs '{"posting_date": "<yyyy-mm-dd>", "company": "<company-name>"}'
```

## 2. Output Interpretation

Job output (`generate_daily_draft_settlements`):

- company
- created_count
- skipped_count

Service summary output (`generate_draft_settlements_for_date`, `include_summary=true`):

- created_count
- skipped_count
- skip_reason_counts

## 3. Reason Codes

- MISSING_SUPPLIER: Source row missing supplier linkage.
- MISSING_ITEM: Source row missing item_code.
- ALREADY_SETTLED: Source row already linked to a settlement (same row protection).
- EXISTING_DRAFT: Draft already exists for supplier plus posting_date.
- SOURCE_LINKED_TO_OTHER_SETTLEMENT: Source row linked to different settlement; overwrite blocked.

## 4. Guardrails You Must Follow

- Do not manually edit `custom_consignment_settlement` on source rows.
- Do not cancel Delivery Note/Sales Invoice first when linked settlement is submitted.
- Cancel settlement first to clear links safely, then process source cancellation.

## 5. Escalation Paths

- Warehouse data issue: Warehouse Supervisor
- Sales posting/linkage issue: Sales Operations Lead
- Settlement mismatch or repeated skips: Finance Operations Lead
- Approval/reconciliation dispute: Finance Controller

## 6. Fast Triage

- High `skipped_count` with low `created_count`:
  run preview summary and inspect dominant reason code.
- Frequent MISSING_SUPPLIER/MISSING_ITEM:
  route to source transaction owner for correction.
- SOURCE_LINKED_TO_OTHER_SETTLEMENT seen repeatedly:
  reconcile lineage before any rerun.

## 7. Post-Restart Smoke Check (Admin)

Use this only after `docker-compose down` plus `docker-compose up -d`.

```bash
docker-compose exec backend bench --site frontend execute frappe.get_installed_apps
docker-compose exec backend bench --site frontend execute client_customizations.consignment.services.readiness.run_consignment_readiness_healthcheck
docker-compose exec backend bench --site frontend execute client_customizations.consignment.services.reconciliation.get_finance_reconciliation_by_scope --kwargs "{'company':'New Horizon','posting_date_from':'2026-07-01','posting_date_to':'2026-07-31','tolerance':0.0}"
```

Expected result:

- App list includes `client_customizations`.
- Readiness returns PASS.
- Reconciliation returns MATCH with zero delta.
