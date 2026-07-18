---
name: frappe-customization-guardrails
description: "Frappe customization guardrails for safe implementation. Use when adding business logic, selecting hooks, and writing server-side changes without touching ERPNext core. Keywords: hook choice, before_save, after_insert, on_submit, custom app, native frappe api."
argument-hint: "Describe customization goal, target DocType/event, and expected behavior"
user-invocable: true
---

# Frappe Customization Guardrails

## When To Use

- Implementing custom business logic
- Choosing lifecycle hook points
- Refactoring unsafe patterns to native Frappe APIs

## Non-Negotiable Rules

- Do not modify Frappe/ERPNext core.
- Keep customizations in a custom app.
- Use native Frappe APIs only:
  - frappe.db.get_value
  - frappe.get_doc
  - frappe.get_list
  - frappe.db.set_value

## Hook Selection Guide

- before_save: enforce/normalize values before persistence
- after_insert: side effects that require a created record
- on_submit: locked-state business actions at finalization

## Procedure

1. Discover existing DocType hooks, services, and workflow touchpoints related to the requirement.
2. Map requirement to the smallest hook surface using current module behavior.
3. Implement with native API calls only.
4. Explain why the selected hook is correct.
5. Provide deterministic bench validation steps.

## Expected Output

- Chosen hook with rationale
- Existing touchpoints discovered and reuse decision
- API usage rationale
- Validation commands and pass criteria
