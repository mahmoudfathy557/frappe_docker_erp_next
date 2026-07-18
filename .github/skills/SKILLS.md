# Skill Registry

## Core Skills

| Skill | Purpose | Default Invoker |
| --- | --- | --- |
| erpnext-doc-operations | list/get/create/update/submit/cancel/delete with verification | ERPNext Operator |
| frappe-customization-guardrails | hook/API constraints and customization safety | Frappe Customizer |
| frappe-docker-bench-ops | command-first Docker bench execution and diagnostics | ERPNext Operator |
| frappe-test-runner | Docker bench unit test execution and failure triage | ERPNext QA Tester |
| erpnext-code-review | structured hook/API/OWASP/test checklist for custom app files | ERPNext Reviewer |
| agent-handoff-contract | structured inter-agent handoff block parsed by pipeline coordinators | Change Pipeline, sub-orchestrators |

## Skill Invocation Order

1. Determine intent category.
2. Run read-only discovery to identify existing module touchpoints.
3. Load domain skill.
4. Apply guardrail skill where mutation is possible.
5. Execute with MCP-first path and bench fallback policy.
6. Validate and report evidence.

## Codebase Knowledge Baseline

1. Prefer integrating existing DocType workflows and hooks before introducing new logic.
2. Every mutating workflow must report what was reused and what was newly added.

## Review and QA Invocation Order

1. After any Frappe Customizer change, invoke erpnext-code-review skill via ERPNext Reviewer.
2. After code review passes, invoke frappe-test-runner skill via ERPNext QA Tester.
3. Only after green tests does the change proceed to ERPNext Operator validation.

## Change Pipeline Skill Usage

1. Change Pipeline coordinator loads agent-handoff-contract skill to parse gate decisions.
2. Each stage agent (Customizer, Reviewer, QA Tester, Operator) must emit the contract block.
3. Pipeline parses GATE_MET field — not prose — to advance, return, or halt.
