---
name: agent-handoff-contract
description: "Structured handoff contract for agent pipeline sequencing. Use when an agent completes a stage and must pass context to the next agent in a pipeline. Keywords: handoff, pipeline contract, gate output, next agent, stage result."
argument-hint: "Fill all fields; set STATUS to FAIL and NEXT_AGENT to the originating agent when a gate is not met"
user-invocable: false
---

# Agent Handoff Contract

## When To Use

Every agent participating in a pipeline must produce this contract block as the final section of its output. The pipeline coordinator parses `GATE_MET` to decide advance, return, or halt — it never infers the decision from prose.

## Contract Format

```
---HANDOFF---
STATUS:          PASS | FAIL | NEEDS-REVIEW | BLOCKED
AGENT:           <agent name>
STAGE:           <Code Change | Review | QA | Deployment Validation>
OUTPUT_SUMMARY:  <one sentence>
ARTIFACTS:       <comma-separated changed files or DocTypes, or "none">
GATE_MET:        yes | no
NEXT_AGENT:      <agent name, or "pipeline-complete">
BLOCKERS:        <list of blocking issues, or "none">
RETRY_COUNT:     <integer, starts at 0, increments on each return to this stage>
---END-HANDOFF---
```

## Gate Decision Rules

| GATE_MET | STATUS       | Pipeline coordinator action                              |
| -------- | ------------ | -------------------------------------------------------- |
| yes      | PASS         | Advance to NEXT_AGENT                                    |
| yes      | NEEDS-REVIEW | Advance to NEXT_AGENT with findings attached             |
| no       | FAIL         | Return to originating stage agent; increment RETRY_COUNT |
| no       | BLOCKED      | Halt immediately; surface BLOCKERS to user               |
| no       | FAIL         | RETRY_COUNT >= 2: halt and escalate to user              |

## Example: Reviewer passing

```
---HANDOFF---
STATUS:          PASS
AGENT:           ERPNext Reviewer
STAGE:           Review
OUTPUT_SUMMARY:  All checklist items passed; no Critical or High findings.
ARTIFACTS:       client_customizations/consignment/services/reconciliation_service.py
GATE_MET:        yes
NEXT_AGENT:      ERPNext QA Tester
BLOCKERS:        none
RETRY_COUNT:     0
---END-HANDOFF---
```

## Example: Reviewer failing back to Customizer

```
---HANDOFF---
STATUS:          FAIL
AGENT:           ERPNext Reviewer
STAGE:           Review
OUTPUT_SUMMARY:  1 Critical finding: unparameterized frappe.db.sql at line 42.
ARTIFACTS:       client_customizations/consignment/services/reconciliation_service.py
GATE_MET:        no
NEXT_AGENT:      Frappe Customizer
BLOCKERS:        A03 Injection risk — reconciliation_service.py:42 uses f-string in frappe.db.sql
RETRY_COUNT:     0
---END-HANDOFF---
```

## Example: QA failing back to Customizer

```
---HANDOFF---
STATUS:          FAIL
AGENT:           ERPNext QA Tester
STAGE:           QA
OUTPUT_SUMMARY:  1 test failure: TestReconciliation.test_balance_mismatch AssertionError.
ARTIFACTS:       client_customizations/consignment/tests/test_reconciliation_service.py
GATE_MET:        no
NEXT_AGENT:      Frappe Customizer
BLOCKERS:        test_balance_mismatch — expected 0 got 150.0 — reconciliation_service.py:87
RETRY_COUNT:     0
---END-HANDOFF---
```
