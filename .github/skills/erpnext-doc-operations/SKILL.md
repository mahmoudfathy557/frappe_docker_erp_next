---
name: erpnext-doc-operations
description: "ERPNext document operations workflow. Use for list/get/create/update/submit/cancel/delete tasks on DocTypes, including validation and status checks. Keywords: sales order, delivery note, purchase order, submit, cancel, delete, get doc, list docs."
argument-hint: "State DocType, record ID (if any), operation, filters, and expected output format"
user-invocable: true
---

# ERPNext Document Operations

## When To Use

- Listing records with filters and limits
- Fetching a single document by name/ID
- Creating or updating document fields
- Lifecycle actions: submit, cancel, delete

## Procedure

1. Resolve operation intent: list/get/create/update/lifecycle.
2. Prefer dedicated ERPNext MCP tool for the DocType/action.
3. If no dedicated tool exists, use generic ERPNext doc tools.
4. If MCP is unavailable, use bench fallback and emit one reason code:
   - MCP_UNSUPPORTED_OPERATION
   - MCP_TOOL_UNAVAILABLE
   - MCP_RUNTIME_FAILURE
5. Validate preconditions (docstatus, required fields, dependencies).
6. Execute action.
7. Re-read document or list to verify the final state.

## Safety Checks

- Confirm destructive actions when environment is not clearly development.
- Stop on first hard failure and report exact blocker.
- Report final status in a compact table.

## Expected Output

- Action summary
- Inputs used (doctype/id/filters)
- Result with verification evidence
- Next remediation step when blocked
