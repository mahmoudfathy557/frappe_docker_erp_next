# Consignment Architecture Code Map (3 Layers)

**Purpose**: Help developers navigate the 3-layer architecture and know exactly where to add new features or debug issues.

**Quick Reference**: Dependency rule is strict: `Layer 1 → Layer 2 → Layer 3 → (no upward calls)`.

---

## Layer 1: Interface / Orchestration

**Responsibility**: Hook handlers, scheduler entrypoints, DocType controller glue.  
**Module Paths**:
- `client_customizations.consignment.interface.validations`
- `client_customizations.consignment.interface.jobs`
- `client_customizations.doctype.consignment_settlement.consignment_settlement` (DocType controller)

**Backward-Compatible Entry Points** (for hook paths and existing imports):
- `client_customizations.consignment.validations` → thin wrapper to `interface.validations`
- `client_customizations.consignment.jobs` → thin wrapper to `interface.jobs`

### Interface.Validations

**Called by**:
- Hook: `Purchase Receipt.before_save`
- Hook: `Delivery Note.on_submit`
- Hook: `Sales Invoice.on_submit`
- Hook: `Delivery Note.on_cancel`
- Hook: `Sales Invoice.on_cancel`

**Exported Functions**:
- `validate_purchase_receipt_for_consignment(doc, method=None)`
- `validate_sale_posting_for_consignment(doc, method=None)`
- `validate_sale_cancel_not_linked_to_submitted_settlement(doc, method=None)`

**What It Does**:
1. Checks if document is consignment-marked.
2. Delegates to `client_customizations.consignment.application.validations` for business rule enforcement.
3. Handles Frappe UX (error messages via `frappe.throw`).

**Where to Add New Validation Logic**:
- If it's a **new hook point** (e.g., new DocType event): add handler here, delegate to `application.*`.
- If it's a **new validation rule**: add it to `application.validations` instead.

### Interface.Jobs

**Called by**: Scheduler (configured in `hooks.py` as `daily` event).

**Exported Functions**:
- `generate_daily_draft_settlements(posting_date=None, dry_run=False, company=None)`

**What It Does**:
1. Collects all companies (or filters to one if scoped).
2. Calls `client_customizations.consignment.application.settlement.generate_draft_settlements_for_date` per company.
3. Aggregates results into compact per-company payload.
4. Returns list of company summaries with created_count, skipped_count.

**Where to Add New Scheduler Tasks**:
- Add new scheduled job handler here.
- Delegate core logic to `application.*` layer.
- Return compact, deterministic payload for observability.

### ConsignmentSettlement DocType Controller

**Path**: `client_customizations.doctype.consignment_settlement.consignment_settlement.py`

**Lifecycle Hooks Wired**:
- `on_submit`: calls `application.payable.ensure_payable_for_submitted_settlement(self)`
- `on_cancel`: calls `application.payable.enforce_settlement_cancel_payable_policy(self)` then clears source links
- `validate`: calls helpers from `application.validations` to check header/row integrity
- `before_save`: normalizes status and computes totals

**Where to Add New Lifecycle Behavior**:
- If new behavior is triggered at a lifecycle event (save, submit, cancel, etc.): add hook here.
- Delegate **all** business logic to `application.*` layer.
- Keep controller focused on Frappe doc mechanics only.

---

## Layer 2: Application / Domain Services

**Responsibility**: Consignment business logic, rules, aggregations, orchestration of domain operations.  
**Module Paths**:
- `client_customizations.consignment.application.settlement`
- `client_customizations.consignment.application.reporting`
- `client_customizations.consignment.application.reconciliation`
- `client_customizations.consignment.application.payable`
- `client_customizations.consignment.application.readiness`
- `client_customizations.consignment.application.validations` (helper validators)

**Backward-Compatible Entry Points** (for existing service imports):
- `client_customizations.consignment.services.settlement` → thin wrapper to `application.settlement`
- `client_customizations.consignment.services.reporting` → thin wrapper to `application.reporting`
- `client_customizations.consignment.services.reconciliation` → thin wrapper to `application.reconciliation`
- `client_customizations.consignment.services.payable` → thin wrapper to `application.payable`
- `client_customizations.consignment.services.readiness` → thin wrapper to `application.readiness`

### Application.Settlement

**Imported by**: Interface, reporting, reconciliation, payable, readiness, tests.

**Key Functions**:
- `generate_draft_settlements_for_date(company, posting_date, supplier=None, dry_run=False, include_summary=False)`
  - Fetch unsettled sale rows from Sales Invoice and Delivery Note.
  - Partition rows into accepted and reason-coded skips.
  - Group by supplier + item.
  - Idempotently create Draft settlements per supplier.
  - Return created list or summary with skip_reason_counts.
  
- `fetch_unsettled_sale_rows(company, posting_date, supplier=None)`
  - Calls `infrastructure.frappe_adapter.get_list()` to fetch consignment sales.
  - Returns normalized row payload.
  
- `mark_source_rows_as_settled(items, settlement_name, dry_run=False)`
  - Updates `custom_consignment_settlement` on source rows.
  - Idempotent: skips rows already linked to another settlement.
  
- `clear_source_rows_settlement_link(items, settlement_name)`
  - Clears `custom_consignment_settlement` on rows where current link equals settlement_name.
  - Used during settlement cancel.

**Pure Helpers** (no DB calls, 100% testable):
- `normalize_settlement_row(row, ...)`
- `partition_settlement_rows_with_reasons(rows)`
- `aggregate_skip_reasons(skipped_rows)`
- `group_rows_by_supplier_item(rows)`
- `split_grouped_lines_by_supplier(grouped_lines)`
- etc.

**Where to Add New Settlement Logic**:
- **New settlement rule or aggregation**: add pure helper function here (test it independently).
- **New data source for settlement rows**: add fetcher function that uses `infrastructure` adapters and returns normalized rows.
- **New settlement lifecycle event**: add to controller, delegate core logic here.

### Application.Reporting

**Imported by**: Interface (bench commands), reconciliation, tests.

**Key Functions**:
- `get_sold_not_settled_summary_by_scope(company, supplier=None, item_code=None, posting_date_from=None, posting_date_to=None)`
  - Fetches unsettled rows for scope.
  - Returns summary: total_qty, total_amount, by_supplier_item, by_posting_date, skipped_count.
  
- `get_settlement_status_exposure(company, supplier=None, posting_date_from=None, posting_date_to=None)`
  - Queries Consignment Settlement status (Draft, Submitted, Cancelled).
  - Returns by_supplier_date buckets and status_totals.

**Pure Helpers**:
- `make_scope_filters(company, supplier, dates...)`
- `bucket_numeric_rows(rows, group_fields, qty_field, amount_field)`
- `build_sold_not_settled_dataset(rows, skipped_rows=None)`
- `build_settlement_status_exposure_dataset(rows)`

**Where to Add New Reporting Metrics**:
- **New report data set**: create pure helper function to compute it.
- **New scope filter or bucketing strategy**: add pure helper, test independently.
- **New runtime report command**: add function here, expose via wrapper for bench execute.

### Application.Reconciliation

**Imported by**: Interface (bench commands), tests.

**Key Functions**:
- `get_finance_reconciliation_by_scope(company, supplier=None, item_code=None, posting_date_from=None, posting_date_to=None, tolerance=0.0)`
  - Composes reporting and reconciliation helpers.
  - Compares sold-not-settled amount vs. draft settlement amount.
  - Returns reconciliation status (MATCH/MISMATCH), deltas, indicators.

**Pure Helpers**:
- `reconcile_sold_not_settled_with_draft_exposure(sold_summary, settlement_exposure, tolerance)`
- `build_reconciliation_indicators(sold_amount, draft_amount, delta, ...)`
- `aggregate_overall_status(checks)` (used for readiness, too)

**Where to Add New Reconciliation Checks**:
- **New reconciliation metric**: add pure helper function.
- **New indicator rule**: add to `build_reconciliation_indicators`.
- **New reconciliation entrypoint**: add function here, wrap for bench command.

### Application.Payable

**Imported by**: Interface (settlement controller), tests.

**Key Functions**:
- `ensure_payable_for_submitted_settlement(settlement_doc)`
  - Idempotently creates one Draft Purchase Invoice per submitted settlement.
  - Links PI back to settlement and updates payable_status.
  - Uses `infrastructure` adapters for doc creation/lookup.
  
- `enforce_settlement_cancel_payable_policy(settlement_doc)`
  - Blocks cancel if linked PI is submitted (policy: finance-safe).
  - Deletes draft PI if present.
  - Keeps cancelled PI linkage state.

**Pure Helpers**:
- `payable_status_from_docstatus(docstatus)`
- `should_create_payable_for_settlement(linked_invoice, existing_marker)`
- `should_block_settlement_cancel_for_payable_docstatus(docstatus)`
- `build_purchase_invoice_payload_from_settlement(settlement_doc)`
- `build_purchase_invoice_items_from_settlement_items(items)`

**Where to Add New Payable Logic**:
- **New payable rule**: add pure helper, test independently.
- **New policy during settlement lifecycle**: add to ensure/enforce functions.
- **New financial document generation**: create application function, call `infrastructure` adapters.

### Application.Readiness

**Imported by**: Interface (bench commands), tests.

**Key Functions**:
- `run_consignment_readiness_healthcheck()`
  - Checks for required DocTypes (Consignment Agreement, Settlement, etc.).
  - Checks for required Custom Fields.
  - Verifies hook configuration against expected bindings.
  - Returns payload: overall_status (PASS/WARN/FAIL), checks list with missing_items.

**Pure Helpers**:
- `build_readiness_payload(existing_doctypes, existing_custom_fields, actual_doc_events, actual_scheduler_events)`
- `aggregate_overall_status(checks)`
- `_find_missing_doc_event_bindings(expected, actual)`
- `_find_missing_scheduler_bindings(expected, actual)`

**Where to Add New Readiness Checks**:
- **New infrastructure requirement**: add check to `build_readiness_payload`.
- **New hook dependency**: add to EXPECTED_*_HOOKS constants and comparison logic.
- **New status aggregation rule**: modify `aggregate_overall_status`.

### Application.Validations

**Imported by**: Interface (validations), tests.

**Key Functions**:
- Purely deterministic validation helpers used by interface validators.
- Examples: `is_consignment_doc()`, `get_items_missing_warehouse()`, `get_rows_missing_supplier_link()`.

---

## Layer 3: Infrastructure / Adapters

**Responsibility**: Wrap Frappe runtime APIs; used exclusively by Layer 2.  
**Module Path**:
- `client_customizations.consignment.infrastructure.frappe_adapter`

**Exported Adapters**:

```python
# List queries
def get_list(doctype, fields=None, filters=None, limit_page_length=0, order_by=None):
    """Wraps frappe.get_list with standard error handling."""
    
# Document retrieval and mutation
def get_doc(doctype, name):
    """Wraps frappe.get_doc for safe document access."""
    
def db_get_value(doctype, name, field):
    """Wraps frappe.db.get_value for single-field queries."""
    
def db_set_value(doctype, name, field, value):
    """Wraps frappe.db.set_value for single-field updates."""
    
# Error handling
def throw(message):
    """Wraps frappe.throw for user-safe error messages."""
```

**Dependency Rule**: Only Layer 2 modules call these adapters; Layer 1 can call Layer 2 if needed, but not Infrastructure directly.

**Where to Add New Infrastructure Capabilities**:
- **New Frappe API access pattern**: add adapter function here.
- **Custom error handling or retry logic**: encapsulate in adapter.
- **Mock/stub for testing**: replace adapter import in tests.

---

## Call Flow Examples

### Example 1: Daily Settlement Generation (End-to-End)

```
Scheduler fires → Interface.Jobs.generate_daily_draft_settlements()
  ├─ Loop companies
  └─→ Application.Settlement.generate_draft_settlements_for_date()
      ├─→ Infrastructure.Adapter.get_list() [fetch unsettled sales]
      ├─→ Application.Settlement.partition_settlement_rows_with_reasons() [pure]
      ├─→ Application.Settlement.group_rows_by_supplier_item() [pure]
      ├─→ Application.Settlement.split_grouped_lines_by_supplier() [pure]
      ├─→ Infrastructure.Adapter.get_doc() [create PI draft per supplier]
      └─→ Infrastructure.Adapter.db_set_value() [link source rows]
  └─ Return compact summary (created_count, skipped_count, skip_reason_counts)
```

### Example 2: Settlement Submit (Payable Generation)

```
User submits Consignment Settlement → DocType Controller.on_submit()
  └─→ Application.Payable.ensure_payable_for_submitted_settlement()
      ├─→ Application.Payable.should_create_payable_for_settlement() [pure]
      ├─→ Infrastructure.Adapter.get_list() [check for existing PI marker]
      ├─→ Application.Payable.build_purchase_invoice_payload_from_settlement() [pure]
      ├─→ Infrastructure.Adapter.get_doc() [create PI]
      └─→ Infrastructure.Adapter.db_set_value() [update settlement link]
```

### Example 3: Settlement Cancel (Reverse Links + Payable Policy)

```
User cancels Consignment Settlement → DocType Controller.on_cancel()
  ├─→ Application.Payable.enforce_settlement_cancel_payable_policy()
  │   ├─→ Application.Payable.should_block_settlement_cancel_for_payable_docstatus() [pure]
  │   ├─→ Infrastructure.Adapter.get_doc() [fetch/delete draft PI if needed]
  │   └─→ Infrastructure.Adapter.db_set_value() [clear link/status]
  └─→ Application.Settlement.clear_source_rows_settlement_link()
      └─→ Infrastructure.Adapter.db_set_value() [clear custom_consignment_settlement]
```

### Example 4: Finance Reconciliation (Reporting + Comparison)

```
User runs: bench --site <site> execute client_customizations.consignment.services.reconciliation.get_finance_reconciliation_by_scope
  └─→ Interface.reconciliation entrypoint wrapper
      └─→ Application.Reconciliation.get_finance_reconciliation_by_scope()
          ├─→ Application.Reporting.get_sold_not_settled_summary_by_scope()
          │   ├─→ Infrastructure.Adapter.get_list() [Sales Invoice items]
          │   ├─→ Infrastructure.Adapter.get_list() [Delivery Note items]
          │   └─→ Application.Reporting.build_sold_not_settled_dataset() [pure]
          ├─→ Application.Reporting.get_settlement_status_exposure()
          │   ├─→ Infrastructure.Adapter.get_list() [Consignment Settlements]
          │   └─→ Application.Reporting.build_settlement_status_exposure_dataset() [pure]
          └─→ Application.Reconciliation.reconcile_sold_not_settled_with_draft_exposure() [pure]
              └─→ Application.Reconciliation.build_reconciliation_indicators() [pure]
```

---

## Adding a New Feature: Decision Tree

**Step 1: Determine scope**
- Is it a **hook/command** (e.g., new lifecycle event, new scheduler job)? → Start in **Layer 1**.
- Is it a **business rule/calculation** (e.g., new skip reason, new reporting metric)? → Start in **Layer 2**.
- Is it **Frappe API access** (e.g., new DB pattern)? → Add to **Layer 3**, then use from Layer 2.

**Step 2: Implement in isolation (if possible)**
- Write pure helper function first (100% testable, no Frappe calls).
- Add unit tests.
- Then wire into orchestration layers.

**Step 3: Wire upward (never downward)**
- Layer 1 calls Layer 2.
- Layer 2 calls Layer 3.
- Tests can import and test any layer independently.

**Step 4: Update docs**
- Add your function to this code map if it's a new integration point.
- Link new behavior to existing tests so maintainers understand intent.

---

## Testing Strategy by Layer

### Layer 1 Integration Tests
- Mock Layer 2 calls.
- Verify orchestration and error handling.
- Example: `test_interface_validations.py` mocks `application.validations` calls.

### Layer 2 Unit Tests
- Test pure helpers with fixtures (no DB).
- Test application functions with mocked infrastructure adapters.
- Example: `test_settlement_service.py` tests pure aggregation logic in isolation.

### Layer 3 Adapter Tests
- Minimal; adapters are thin wrappers.
- Focus on error handling consistency.

---

## Import Examples

**Correct (Layer 2 to Layer 3)**:
```python
# application/settlement.py
from client_customizations.consignment.infrastructure.frappe_adapter import get_list, db_set_value

def generate_draft_settlements_for_date(company, posting_date, ...):
    rows = get_list("Sales Invoice Item", filters=..., fields=...)
    db_set_value("Sales Invoice Item", row_name, "custom_consignment_settlement", settlement_name)
```

**Correct (Layer 1 to Layer 2)**:
```python
# interface/validations.py
from client_customizations.consignment.application.validations import is_consignment_doc

def validate_purchase_receipt_for_consignment(doc, method=None):
    if not is_consignment_doc(doc):
        return
    # ... call other application helpers
```

**Incorrect (Layer 2 calling Layer 1)**:
```python
# application/settlement.py (BAD)
from client_customizations.consignment.interface.validations import validate_purchase_receipt_for_consignment
# ✗ This creates upward dependency!
```

---

## Where to Find Things

| Feature | Layer 1 | Layer 2 | Layer 3 |
|---------|---------|---------|---------|
| Hook handler | `interface.validations` | Application helpers | N/A |
| Scheduler job | `interface.jobs` | Application service | N/A |
| Business rule | ├─ Orchestration | `application.*` | N/A |
| Data aggregation | N/A | Pure helper functions | N/A |
| Frappe API call | N/A | N/A | `infrastructure.frappe_adapter` |
| New report metric | N/A | `application.reporting` | N/A |
| New validation | N/A | `application.validations` | N/A |
| New reconciliation check | N/A | `application.reconciliation` | N/A |

---

## Next Steps for Your Team

1. **Onboarding**: Read this code map, then read `technical_blueprint.md` for business context.
2. **Adding a feature**: Follow "Decision Tree" section above.
3. **Debugging**: Trace call flow using examples in this document; error logs will show which layer failed.
4. **Testing**: Write pure helper tests first (Layer 2), then integration tests (Layer 1).
5. **Maintenance**: Keep Layer 1/2 dependency strict; never let Layer 2 call Layer 1 or Layer 3 call Layer 2.
