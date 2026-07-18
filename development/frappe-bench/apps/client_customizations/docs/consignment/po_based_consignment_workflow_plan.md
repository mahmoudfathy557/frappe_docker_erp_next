# PO-Based Consignment Workflow Plan

Status: Draft for implementation and UAT  
Owner: Finance and Supply Chain  
Scope: ERPNext consignment process with mandatory Purchase Order control

## 1. Final Business Rules

1. Purchase Order is mandatory for all consignment receipts.
2. Price is fixed on Purchase Order.
3. Over-receipt is not allowed.
4. Partial and full receipt are allowed.
5. Four main consignment warehouses will be created.
6. Cancellation must be sequential:
   1. Cancel Sales Invoice first.
   2. Cancel Purchase Receipt second.
   3. Cancel Purchase Order last.

## 2. Target Workflow

1. Create Consignment Agreement with supplier.
2. Create Consignment Purchase Order.
3. Receive goods using Purchase Receipt against Purchase Order.
4. Sell goods using Sales Invoice from consignment stock.
5. Generate Consignment Settlement from sold quantity and amount.
6. On settlement submit, create draft Purchase Invoice payable to supplier.
7. Finance reviews and posts payable.

## 3. System Controls and Validation Policy

## 3.1 Purchase Order Controls

1. Consignment flag is required for consignment Purchase Orders.
2. Supplier is required.
3. Warehouse must be one of approved consignment warehouses.
4. Rate on PO is authoritative for downstream valuation and settlement reference.

## 3.2 Purchase Receipt Controls

1. Purchase Receipt must reference a Purchase Order for consignment flow.
2. Over-receipt is blocked.
3. Partial receipt is allowed.
4. Full receipt is allowed.
5. Price deviation from Purchase Order is blocked.

## 3.3 Sales Invoice Controls

1. Sales line must trace to valid consignment stock lineage.
2. Sales posting against invalid or unlinked consignment source is blocked.

## 3.4 Settlement Controls

1. Settlement uses sold rows linked to consignment source chain.
2. One draft settlement per supplier and posting date.
3. Idempotent rerun behavior is required to avoid duplicate linking.

## 3.5 Cancellation Controls

1. Purchase Receipt cancellation is blocked if linked Sales Invoice is not canceled.
2. Purchase Order cancellation is blocked if linked Purchase Receipt is not canceled.
3. Error messages must state the next required cancellation step.

## 4. Warehouse Structure

Create and maintain four dedicated consignment warehouses:

1. Consignment Raw Materials
2. Consignment Finished Goods
3. Consignment Trading Items
4. Consignment Returns Hold

Notes:

1. Do not use non-consignment warehouses for consignment transactions.
2. For multi-branch or multi-company, replicate the same four-warehouse model per unit.

## 5. Document Dependency Chain

Use this strict dependency chain for traceability and controls:

1. Purchase Order
2. Purchase Receipt
3. Sales Invoice
4. Consignment Settlement
5. Purchase Invoice payable

## 6. Exception and Blocking Scenarios

1. Receipt without Purchase Order: blocked.
2. Over-receipt attempt: blocked.
3. Price mismatch against PO: blocked.
4. Attempt to cancel Purchase Receipt before Sales Invoice cancellation: blocked.
5. Attempt to cancel Purchase Order before Purchase Receipt cancellation: blocked.

## 7. Edge Cases and Expected Behavior

1. Partial receipt across multiple days:
   1. Scenario: same PO is received in multiple PRs over different posting dates.
   2. Expected: allowed, cumulative received quantity cannot exceed ordered quantity.
2. Duplicate PR submission click or retry:
   1. Scenario: user retries submit due to latency.
   2. Expected: system remains idempotent and does not double-post stock.
3. Same item in multiple PO rows:
   1. Scenario: item repeated by schedule or batch split.
   2. Expected: PR row must map to correct PO row reference, quantity checks apply per mapped line.
4. Late sales posting after period close:
   1. Scenario: Sales Invoice posts in next period for stock received in prior period.
   2. Expected: settlement picks posting date logic consistently and reconciliation highlights period variance.
5. Currency and exchange-rate differences:
   1. Scenario: PO in foreign currency, base currency changes by rate date.
   2. Expected: PO line rate policy remains authoritative in transaction currency; base amount conversion follows accounting rate rules.
6. Supplier changed after PO creation:
   1. Scenario: user attempts to use different supplier in PR or downstream chain.
   2. Expected: blocked for consignment flow; supplier lineage must remain consistent.
7. Warehouse mismatch in consignment flow:
   1. Scenario: PR or stock movement tries non-consignment warehouse with consignment marker.
   2. Expected: blocked and user prompted to use approved consignment warehouse.
8. Return or negative quantity handling:
   1. Scenario: return transaction is created after sale or receipt correction.
   2. Expected: routed to consignment returns hold warehouse and excluded from normal settlement run unless explicitly included by policy.
9. Backdated cancellation sequence:
   1. Scenario: user cancels SI in a later period and tries PR cancel with earlier posting date.
   2. Expected: sequence enforcement still applies; period control warnings raised if accounting period rules are violated.
10. Settlement rerun after partial corrections:
   1. Scenario: some source rows are fixed and job is rerun.
   2. Expected: only newly eligible rows are linked; existing valid links are preserved.
11. Concurrent settlement job execution:
   1. Scenario: scheduler and manual run overlap.
   2. Expected: locking/idempotency prevents duplicate draft settlements for same supplier and date.
12. Canceled source relinking risk:
   1. Scenario: source row was linked to old settlement then corrected.
   2. Expected: relinking only allowed after proper cancel sequence, and only to the current valid settlement.

## 8. UAT Scenarios and Expected Outcomes

1. Happy path:
   1. PO -> partial PR -> SI -> Settlement -> draft PI
   2. Expected: pass
2. Full receipt path:
   1. PO -> full PR -> SI -> Settlement
   2. Expected: pass
3. Over-receipt attempt:
   1. PR quantity exceeds PO balance
   2. Expected: blocked
4. Receipt without PO attempt:
   1. PR created without PO link
   2. Expected: blocked
5. Price mismatch attempt:
   1. PR or downstream valuation differs from PO rate
   2. Expected: blocked
6. Wrong cancellation sequence:
   1. Cancel PR before SI cancellation
   2. Expected: blocked
7. Correct cancellation sequence:
   1. Cancel SI -> cancel PR -> cancel PO
   2. Expected: pass

## 9. Go-Live Checklist

1. Four consignment warehouses created and active.
2. Role permissions configured for Buying, Warehouse, Sales, and Finance users.
3. Validation rules enabled for PO, PR, SI, settlement, and cancellation sequence.
4. UAT scenarios executed with evidence and sign-off.
5. User guides published for English and Arabic users.

## 10. Ownership and Escalation

1. Process owner: Finance and Supply Chain lead.
2. System owner: ERP application owner.
3. Escalation order:
   1. Business process lead
   2. ERP functional lead
   3. ERP technical support
