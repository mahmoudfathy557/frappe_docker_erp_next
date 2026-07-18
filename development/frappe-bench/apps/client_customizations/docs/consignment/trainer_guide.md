# Consignment Trainer Guide

Status: Trainer-ready  
Audience: Internal trainers for Warehouse, Sales, and Finance users

## 1. Session Agenda (120 minutes)

1. Business context and scope (10 min)
2. Role overview and controls (15 min)
3. Guided demo (Warehouse, Sales, Finance) (45 min)
4. Hands-on exercises (35 min)
5. Debrief: mistakes, escalation, readiness sign-off (15 min)

## 2. Learning Objectives

By end of session, learners can:

- Enter consignment transactions with correct marker/supplier linkage.
- Run and interpret settlement generation outputs.
- Explain why cancel order matters for safe reversals.
- Resolve common skip reasons with correct escalation.

## 3. Demo Script

Use one company and one supplier for a clean first run, then include one intentional error for coaching.

## A. Warehouse flow demo

1. Open Purchase Receipt and set consignment marker.
2. Ensure header supplier is present.
3. Show that missing warehouse on item blocks save.
4. Save successfully after fixing missing warehouse.

Trainer callout:

- before_save validation protects data quality before stock flow continues.

## B. Sales flow demo

1. Open Delivery Note or Sales Invoice with consignment marker.
2. Submit once with missing supplier linkage on a row to trigger error.
3. Correct linkage and submit successfully.
4. Show resulting source rows are candidates for settlement generation.

Trainer callout:

- on_submit validation enforces supplier linkage at authoritative posting point.

## C. Finance flow demo

1. Run preview summary for one company/date:

```bash
bench --site <site-name> execute client_customizations.consignment.services.settlement.generate_draft_settlements_for_date --kwargs '{"company": "<company-name>", "posting_date": "<yyyy-mm-dd>", "dry_run": true, "include_summary": true}'
```

2. Explain created_count, skipped_count, and skip_reason_counts.
3. Run actual daily generation (job entrypoint).
4. Open created Draft settlement and verify row/header integrity.
5. Submit settlement as Finance Controller.
6. Attempt to cancel linked source sale doc and show guard message.
7. Cancel settlement first; explain link clearing behavior.

Trainer callout:

- Guardrail prevents unsafe source cancellation while linked settlement is submitted.
- Cancellation clears link only for rows linked to the exact cancelled settlement.

## 4. Hands-On Exercises

## Exercise 1: Happy-path settlement generation

Task:

- Create consignment sale postings for one posting date.
- Run job generation for that date.

Expected outcome:

- Draft settlement created by supplier.
- Source rows linked through `custom_consignment_settlement`.

## Exercise 2: Data-quality skip reasons

Task:

- Create one source row missing supplier linkage and one missing item code scenario.
- Run service preview (`include_summary=true`).

Expected outcome:

- skip_reason_counts includes MISSING_SUPPLIER and/or MISSING_ITEM.
- No settlement line created from invalid source rows.

## Exercise 3: Idempotency and existing draft handling

Task:

- Generate draft once for supplier/date, then re-run generation.

Expected outcome:

- No duplicate draft for same supplier/date.
- Existing run reports skip pattern consistent with EXISTING_DRAFT logic.

## Exercise 4: Safe cancellation sequence

Task:

- Submit settlement, then attempt source sales cancellation.
- Cancel settlement first, then cancel source sales doc.

Expected outcome:

- Initial source cancel is blocked while settlement submitted.
- After settlement cancel, source link clears and cancellation can proceed.

## 5. Common Mistakes and Coaching Notes

- Mistake: Running only job command and expecting reason-code map.
  Coach: reason-code detail is from service-level summary (`include_summary=true`), while job output is compact per company.

- Mistake: Manual edit of `custom_consignment_settlement` on source rows.
  Coach: use settlement lifecycle only; manual edits break lineage integrity.

- Mistake: Canceling Delivery Note/Sales Invoice before settlement cancel.
  Coach: always reverse settlement first to trigger safe link clearing.

- Mistake: Treating skipped rows as system failure.
  Coach: skip reasons are protective controls; investigate and resolve root cause.

## 6. Readiness Checklist

Use this checklist per learner group:

- Can create consignment Purchase Receipt with valid supplier and warehouses.
- Can submit consignment Delivery Note/Sales Invoice with supplier linkage.
- Can run both preview (service) and execution (job) commands.
- Can interpret created_count, skipped_count, and skip_reason_counts.
- Can explain and execute correct cancel/rebuild sequence.
- Can route issues through escalation path correctly.

## 7. Sign-off Template

```text
Consignment Enablement Sign-off

Team/Location:
Session Date:
Trainer:

Participants:
-
-
-

Checklist Result (Pass/Needs Follow-up):
- Warehouse operation competency:
- Sales posting competency:
- Finance generation/review competency:
- Guardrail and cancel sequence competency:

Open Risks:
-

Follow-up Actions:
-

Trainer Signature:
Operations Owner Signature:
Finance Owner Signature:
```
