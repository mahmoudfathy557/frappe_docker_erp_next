# Consignment Customization Technical Blueprint (Slice 5)

Status: Resilience hardening with reason-coded skip telemetry and cancellation/reversal guardrails
Scope: Custom app only (no ERPNext/Frappe core edits)

## 1. Target Model

This customization keeps ERPNext core purchase and sales behavior unchanged and adds a controlled consignment settlement flow.

- Core cycle: unchanged ERPNext purchasing/sales lifecycle.
- Consignment cycle: receive and sell stock first, then settle supplier by sold-not-settled rows.

### Architecture (3 Layers)

This implementation follows an explicit 3-layer structure in the custom app package:

- Layer 1: Interface/Orchestration
	- Module paths: `client_customizations.consignment.interface.*`
	- Responsibilities: hook handlers, scheduler/job entrypoints, DocType controller orchestration.
	- Compatibility entrypoints kept: `client_customizations.consignment.validations` and `client_customizations.consignment.jobs`.
- Layer 2: Application/Domain Services
	- Module paths: `client_customizations.consignment.application.*`
	- Responsibilities: settlement, reporting, reconciliation, payable, readiness business rules.
	- Compatibility entrypoints kept: `client_customizations.consignment.services.*` thin wrappers.
- Layer 3: Infrastructure/Adapters
	- Module paths: `client_customizations.consignment.infrastructure.*`
	- Responsibilities: wrappers over Frappe runtime APIs (`get_list`, `get_doc`, `db.get_value`, `db.set_value`, `throw`) used by the application/interface layers.

Operational runbook alignment:

- Daily operations and command entrypoints: `docs/consignment/runbook.md`
- Quick command reference: `docs/consignment/operator_quick_reference.md`

## 2. Current Guarantees

### 2.1 Settlement Controller Safety

`Consignment Settlement` now enforces:

- Header must include supplier.
- At least one item row is required.
- Every row must include supplier and item_code.
- Every row supplier must exactly match header supplier.
- Every row qty must be strictly greater than 0.
- Every row base_amount must be greater than or equal to 0.
- Invalid status values are blocked.

Validation failures use `frappe.throw`, so users receive business-safe messages in normal Frappe UX.

### 2.2 Canonical Settlement Row Schema

Service internals now normalize all sale row payloads to one shape before grouping/aggregation:

- sales_doctype
- sales_document
- sales_row
- supplier
- item_code
- qty
- base_amount
- custom_consignment_settlement

This removes inconsistent amount-path handling between different helper paths.

### 2.3 Idempotent Source Marking

When marking source rows with settlement references:

- Duplicate attempts in same call are deduplicated by (sales_doctype, sales_row).
- Rows already linked to another settlement are skipped (not overwritten).
- Rows already linked to the same settlement are skipped (no redundant write).
- Marking returns compact marked/skip counters for operational observability.

### 2.4 Scheduler/Manual Job Consistency

Daily generation entrypoint supports both:

- Scheduler default: all companies.
- Manual scoped run: optional company filter.

Job return payload is compact by company:

- company
- created_count
- skipped_count

### 2.5 Reason-Coded Skip Telemetry

Settlement generation and source-linking now emit reason-coded skip counters for deterministic reporting.

Supported reason codes:

- MISSING_SUPPLIER
- MISSING_ITEM
- ALREADY_SETTLED
- EXISTING_DRAFT
- SOURCE_LINKED_TO_OTHER_SETTLEMENT

Behavior:

- Legacy callers remain compatible: generation still returns a created list by default.
- Summary mode (`include_summary=True`) now includes `skip_reason_counts` map.
- Canonical row partitioning is done before grouping so invalid/settled rows are counted consistently.

### 2.6 Cancellation/Reversal Semantics (v1)

Consignment Settlement cancel path now reverses source links safely:

- Trigger point: `Consignment Settlement.on_cancel`.
- Action: clear `custom_consignment_settlement` on source rows only if the current source link equals the cancelling settlement name.
- Safety: rows linked to other settlements are never overwritten.
- Idempotency: repeated cancel logic does not produce destructive side effects.

Sales cancellation guardrails:

- Trigger point: `Delivery Note.on_cancel` and `Sales Invoice.on_cancel` hooks.
- Action: block cancel when any linked settlement is submitted.
- Message instructs finance-safe order of operations: cancel submitted settlement(s) first, which clears links, then cancel source sales doc.

### 2.7 Settlement Payable Generation (v1)

Consignment Settlement submit now creates one linked supplier payable draft:

- Trigger point: `Consignment Settlement.on_submit`.
- Action: create Draft `Purchase Invoice` from settlement header and item rows.
- Linkage: settlement stores `linked_purchase_invoice` and `payable_status`; payable stores `custom_consignment_settlement` marker.
- Idempotency: if settlement already has a valid linked payable or an existing payable with the same settlement marker exists, no duplicate payable is created.

Settlement cancel payable policy (safe v1):

- If linked payable is submitted: block settlement cancel with clear action message.
- If linked payable is draft: delete draft payable and clear settlement link/state.
- If linked payable is cancelled: settlement cancel proceeds without mutating cancelled payable.

## 3. Known Constraints

- Settlement generation is keyed by supplier + posting_date draft existence; it does not yet handle versioned reruns after post-close corrections.
- Reason-coded telemetry is counter-based and intentionally compact; row-level audit export is not yet included.
- Return/credit-note accounting workflow integration is outside this slice.
- Automatic payable submission is intentionally deferred; v1 generates deterministic draft payable for finance review.

## 4. Hook Choice and Rationale

- Purchase Receipt uses before_save for early data quality checks.
- Delivery Note and Sales Invoice use on_submit because consignment sale linkage is authoritative at final posting.
- Delivery Note and Sales Invoice also use on_cancel to block unsafe cancellation when linked to submitted settlements.
- Consignment Settlement DocType validation protects integrity at save time where settlement lines are authored.
- Consignment Settlement uses on_submit for payable generation so payable creation happens only at finalized settlement lifecycle.
- Consignment Settlement uses on_cancel to execute reversal (source-link clear) at the exact lifecycle point where cancellation is confirmed.

## 5. Verification Commands

Run from app root in backend/container shell.

```bash
python -m unittest client_customizations.consignment.tests.test_settlement_service -v
python -m unittest client_customizations.consignment.tests.test_payable_service -v
python -m unittest client_customizations.consignment.tests.test_validations_helpers -v
python -m unittest client_customizations.consignment.tests.test_jobs_helpers -v
```

Manual dry-run execution:

```bash
bench --site <site-name> execute client_customizations.consignment.jobs.generate_daily_draft_settlements --kwargs '{"dry_run": true}'
bench --site <site-name> execute client_customizations.consignment.jobs.generate_daily_draft_settlements --kwargs '{"posting_date": "2026-07-18", "company": "<company-name>", "dry_run": true}'

# Optional summary visibility for reason-coded skips
bench --site <site-name> execute client_customizations.consignment.services.settlement.generate_draft_settlements_for_date --kwargs '{"company": "<company-name>", "posting_date": "2026-07-18", "include_summary": true, "dry_run": true}'
```
