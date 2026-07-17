# Skill Registry

## Core Skills

| Skill | Purpose | Default Invoker |
| --- | --- | --- |
| erpnext-doc-operations | list/get/create/update/submit/cancel/delete with verification | ERPNext Operator |
| frappe-customization-guardrails | hook/API constraints and customization safety | Frappe Customizer |
| frappe-docker-bench-ops | command-first Docker bench execution and diagnostics | ERPNext Operator |

## Skill Invocation Order

1. Determine intent category.
2. Load domain skill.
3. Apply guardrail skill where mutation is possible.
4. Execute with MCP-first path and bench fallback policy.
5. Validate and report evidence.
