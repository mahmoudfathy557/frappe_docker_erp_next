---
description: "Governance rules for orchestrated ERPNext agent execution in this repository."
applyTo: ".github/agents/**/*.agent.md"
---

# Orchestration Governance

## Non-Negotiables

1. No edits to Frappe/ERPNext core.
2. Customization work stays in custom apps.
3. Native Frappe APIs only for customization logic:
   - frappe.db.get_value
   - frappe.get_doc
   - frappe.get_list
   - frappe.db.set_value

## Codebase-First Integration

1. Before proposing or executing any customization, identify existing DocTypes, hooks, services, and workflows that already solve part of the requirement.
2. Prefer extending existing module behavior over creating parallel systems.
3. Output must include a short reuse map: existing touchpoints found, what is reused, and what new code is strictly required.
4. If touchpoints are unknown, run a read-only discovery pass before any mutation.

## Environment Mode

1. Development mode: execution allowed with mandatory verification.
2. Production-like mode: require explicit confirmation before mutating actions.

## Verification Standard

1. Every state-changing action must be followed by one read-back verification.
2. Output must include exact tool path used (MCP or bench fallback).
3. If fallback was used, include reason code.
