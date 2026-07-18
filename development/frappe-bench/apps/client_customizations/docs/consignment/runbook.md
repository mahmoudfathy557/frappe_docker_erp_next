# Consignment Operations Runbook

Status: Approved for production operations enablement  
Audience: Warehouse, Sales Operations, Finance Operations, Finance Controller

## 1. Purpose and Scope

This runbook defines how to operate the consignment flow delivered in the custom app.

- In scope: consignment marker and supplier linkage quality, daily draft settlement generation, review and submission controls, safe cancel/rebuild handling.
- Out of scope: ERPNext/Frappe core process changes, return/credit-note automation.

### Architecture (3 Layers)

This runbook operates against a 3-layer implementation in the custom app:

- Layer 1: Interface/Orchestration
	- Hook and scheduler entrypoints remain stable for operations:
		- `client_customizations.consignment.validations.*`
		- `client_customizations.consignment.jobs.generate_daily_draft_settlements`
- Layer 2: Application/Domain Services
	- Settlement/reporting/reconciliation/payable/readiness logic is implemented under:
		- `client_customizations.consignment.application.*`
	- Existing command paths stay valid via wrappers:
		- `client_customizations.consignment.services.*`
- Layer 3: Infrastructure/Adapters
	- Frappe runtime access wrappers are centralized under:
		- `client_customizations.consignment.infrastructure.*`

Reference documents:

- Technical blueprint: `docs/consignment/technical_blueprint.md`
- Operator quick reference: `docs/consignment/operator_quick_reference.md`
- Frontend user setup guide (EN): `docs/consignment/frontend_user_setup_guide_en.md`
- Frontend user setup guide (AR): `docs/consignment/frontend_user_setup_guide_ar.md`
- Frontend user setup guide (EN+AR): `docs/consignment/frontend_user_setup_guide_ar_en.md`

## 2. Role Responsibilities

## Warehouse Operator

- Set consignment marker on Purchase Receipt when applicable.
- Ensure Purchase Receipt has supplier and item warehouses before save.

## Sales Operator

- Submit Delivery Note/Sales Invoice with consignment marker enabled.
- Ensure supplier linkage is present at header and/or item row level before submit.

## Finance Operator

- Run settlement generation for target posting date.
- Review created Draft settlements by supplier and posting date.
- Escalate abnormal skips or data quality gaps.

## Finance Controller

- Approve and submit valid settlements.
- Govern correction cycles (cancel settlement first, then source correction).

## 3. Daily Operating Flow

## Step 1: Pre-batch checks

- Confirm all expected consignment sales docs for the posting date are submitted.
- Confirm supplier data is valid for all expected consignment sales.
- Confirm no active posting edits are in progress for the batch window.

## Step 2: Preview impact (optional but recommended)

Use service-level summary to view reason-coded skip telemetry.

```bash
bench --site <site-name> execute client_customizations.consignment.services.settlement.generate_draft_settlements_for_date --kwargs '{"company": "<company-name>", "posting_date": "<yyyy-mm-dd>", "dry_run": true, "include_summary": true}'
```

Expected summary fields:

- created_count
- skipped_count
- skip_reason_counts

Supported reason codes:

- MISSING_SUPPLIER
- MISSING_ITEM
- ALREADY_SETTLED
- EXISTING_DRAFT
- SOURCE_LINKED_TO_OTHER_SETTLEMENT

## Step 3: Execute daily generation

Manual all-company run:

```bash
bench --site <site-name> execute client_customizations.consignment.jobs.generate_daily_draft_settlements --kwargs '{"posting_date": "<yyyy-mm-dd>"}'
```

Manual single-company run:

```bash
bench --site <site-name> execute client_customizations.consignment.jobs.generate_daily_draft_settlements --kwargs '{"posting_date": "<yyyy-mm-dd>", "company": "<company-name>"}'
```

Expected job payload per company:

- company
- created_count
- skipped_count

Behavioral guarantees:

- At most one Draft settlement per supplier plus posting_date.
- Source link field (`custom_consignment_settlement`) is set only if source row is not already linked to a different settlement.

## Step 4: Review Draft settlements

- Header supplier is present.
- Every row supplier equals header supplier.
- Every row has item_code.
- qty is greater than 0.
- base_amount is greater than or equal to 0.
- Total quantity and amount are reasonable vs. posted sales activity.

## Step 5: Approve and submit

- Finance Controller submits approved settlements.
- Settlement submit auto-generates one Draft Purchase Invoice payable linked back to the settlement.
- Finance reviews generated payable draft amounts/lines before submitting the Purchase Invoice.
- Rejected drafts must be corrected through controlled rebuild cycle.

## 4. Controlled Cancel/Rebuild Procedure

Use this only when already submitted settlement(s) require correction.

1. Identify submitted settlement(s) and affected source sales docs.
2. Cancel settlement(s) first.
3. Correct source data and re-submit source docs as needed.
4. Re-run settlement generation for the posting date.
5. Re-review and submit rebuilt settlements.

Important guardrails:

- Cancelling Delivery Note or Sales Invoice is blocked while linked settlement is submitted.
- Settlement cancel is blocked if linked Purchase Invoice is submitted (cancel PI first, then settlement).
- Settlement cancel auto-deletes linked Draft Purchase Invoice, then clears settlement payable link/state.
- Settlement cancel clears source link only when source row currently links to the cancelling settlement name.
- Links to other settlements are never overwritten by cancel logic.

## 5. Exception Handling

- Missing supplier/item skip reasons: fix source data first, then regenerate.
- Existing draft skip reason: review and reuse current draft where valid.
- Source linked to other settlement: reconcile settlement lineage before rerun.
- Settlement cancel blocked by submitted payable: cancel linked Purchase Invoice first.
- Repeated high skip counts: open process-quality incident with owning function.

## 6. Daily Close Checklist

- Daily run completed for intended posting date (scheduler or manual).
- Drafts reviewed for supplier and line integrity.
- Linked payable drafts reviewed and submitted/corrected per finance approval policy.
- Unexpected skip patterns reviewed and logged.
- Approved drafts submitted per approval policy.
- Exceptions recorded with owner and target resolution date.

## 7. Escalation Routing

- Warehouse data quality: Warehouse Supervisor
- Sales posting quality: Sales Operations Lead
- Settlement generation/data mismatch: Finance Operations Lead
- Approval/reconciliation conflict: Finance Controller

## 8. Platform Durability Verification (Admin)

Use this after container recreation to confirm the consignment app remains operational without manual copy/install actions.

From repository root (`frappe_docker`):

```bash
docker-compose down
docker-compose up -d
docker-compose ps
docker-compose exec backend bench --site frontend execute frappe.get_installed_apps
docker-compose exec backend bench --site frontend execute client_customizations.consignment.services.readiness.run_consignment_readiness_healthcheck
docker-compose exec backend bench --site frontend execute client_customizations.consignment.jobs.generate_daily_draft_settlements --kwargs "{'posting_date':'2026-07-18','dry_run':True}"
docker-compose exec backend bench --site frontend execute client_customizations.consignment.services.reconciliation.get_finance_reconciliation_by_scope --kwargs "{'company':'New Horizon','posting_date_from':'2026-07-01','posting_date_to':'2026-07-31','tolerance':0.0}"
```

Success criteria:

- Installed apps output includes `client_customizations`.
- Readiness output shows `overall_status: PASS`.
- Reconciliation output shows `status: MATCH` and `delta_amount: 0.0`.

Durability prerequisites:

- `.env` defines `ERPNEXT_VERSION`, `DB_HOST`, `DB_PORT`, `REDIS_CACHE`, and `REDIS_QUEUE`.
- `docker-compose.override.yml` mounts `development/frappe-bench/apps/client_customizations` into app services and sets `PYTHONPATH` for Python runtime services.
