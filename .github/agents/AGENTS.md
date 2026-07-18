# Agent Registry

This registry is the source of truth for capability tiers, routing, and delegation contracts.

## Capability Tiers

1. Tier 0: Read-only analysis and routing (Orchestrator, Reviewer)
2. Tier 0.5: Delegation-only coordinators — read/search/agent, no direct execution
3. Tier 1: Safe write operations in development
4. Tier 2: State-changing ERPNext operations in development
5. Tier 3: Production-gated operations with explicit confirmation

## Agent Matrix

### Layer 0 — Top-Level Coordinator

| Agent                | Primary Scope               | Tier Ceiling | Tools Profile       | Delegates To                                                                              |
| -------------------- | --------------------------- | ------------ | ------------------- | ----------------------------------------------------------------------------------------- |
| ERPNext Orchestrator | classification + delegation | Tier 0       | read, search, agent | Change Pipeline, sub-orchestrators, ERPNext Operator, ERPNext Reviewer, ERPNext QA Tester |

### Layer 0.5 — Pipelines and Sub-Orchestrators

| Agent                    | Primary Scope                                                 | Tier Ceiling | Tools Profile       | Delegates To                                                                    |
| ------------------------ | ------------------------------------------------------------- | ------------ | ------------------- | ------------------------------------------------------------------------------- |
| Change Pipeline          | gated change workflow sequencing                              | Tier 0.5     | read, search, agent | Frappe Customizer, ERPNext Reviewer, ERPNext QA Tester, ERPNext Operator        |
| Finance Coordinator      | Accounts + Selling + Buying coordination                      | Tier 0.5     | read, search, agent | Accounts Specialist, Selling Specialist, Buying Specialist, ERPNext Operator    |
| Supply Chain Coordinator | Stock + Manufacturing + Buying coordination                   | Tier 0.5     | read, search, agent | Stock Specialist, Manufacturing Specialist, Buying Specialist, ERPNext Operator |
| People Ops Coordinator   | HR + Projects + CRM coordination                              | Tier 0.5     | read, search, agent | HR Specialist, Projects Specialist, CRM Specialist, ERPNext Operator            |
| Operations Coordinator   | Assets + Support + Quality + Website + Compliance + Reporting | Tier 0.5     | read, search, agent | 6 domain specialists + ERPNext Operator                                         |

### Layer 1 — Core Execution Agents

| Agent             | Primary Scope                         | Tier Ceiling | Tools Profile               | Delegates To                         |
| ----------------- | ------------------------------------- | ------------ | --------------------------- | ------------------------------------ |
| ERPNext Operator  | ERPNext document/data operations      | Tier 3       | read, search, execute       | none                                 |
| Frappe Customizer | custom app code changes and refactors | Tier 3       | read, search, edit, execute | none                                 |
| ERPNext Reviewer  | custom app code audit (read-only)     | Tier 0       | read, search                | Frappe Customizer, ERPNext QA Tester |
| ERPNext QA Tester | test execution and validation         | Tier 1/2     | read, search, execute       | Frappe Customizer, ERPNext Operator  |

### Layer 2 — Domain Specialists

| Agent                          | Primary Scope                 | Tier Ceiling | Tools Profile         | Delegates To |
| ------------------------------ | ----------------------------- | ------------ | --------------------- | ------------ |
| Accounts Specialist            | Accounts workflows            | Tier 3       | read, search, execute | none         |
| Selling Specialist             | Selling workflows             | Tier 3       | read, search, execute | none         |
| Buying Specialist              | Buying workflows (shared)     | Tier 3       | read, search, execute | none         |
| Stock Specialist               | Stock workflows               | Tier 3       | read, search, execute | none         |
| Manufacturing Specialist       | Manufacturing workflows       | Tier 3       | read, search, execute | none         |
| HR Specialist                  | HR workflows                  | Tier 3       | read, search, execute | none         |
| Projects Specialist            | Projects workflows            | Tier 3       | read, search, execute | none         |
| CRM Specialist                 | CRM workflows                 | Tier 3       | read, search, execute | none         |
| Assets Specialist              | Assets workflows              | Tier 3       | read, search, execute | none         |
| Support Specialist             | Support workflows             | Tier 3       | read, search, execute | none         |
| Quality Specialist             | Quality module workflows      | Tier 3       | read, search, execute | none         |
| Website Specialist             | Website workflows             | Tier 3       | read, search, execute | none         |
| Regional Compliance Specialist | Regional/compliance workflows | Tier 3       | read, search, execute | none         |
| Reporting Analytics Specialist | Reporting/analytics workflows | Tier 3       | read, search, execute | none         |

## Deterministic Routing Rules

1. End-to-end code change → Change Pipeline.
2. Code-only change (no gate needed) → Frappe Customizer.
3. Simple document operation → ERPNext Operator.
4. Code review / audit → ERPNext Reviewer.
5. Test execution / QA → ERPNext QA Tester.
6. Finance domain → Finance Coordinator.
7. Supply chain domain → Supply Chain Coordinator.
8. People ops domain → People Ops Coordinator.
9. Operations/support domain → Operations Coordinator.
10. Unknown intent → one clarification question, then route.

## Sub-Orchestrator Coverage

| Coordinator              | Modules                                                                     |
| ------------------------ | --------------------------------------------------------------------------- |
| Finance Coordinator      | Accounts, Selling, Buying (financial)                                       |
| Supply Chain Coordinator | Stock, Manufacturing, Buying (procurement)                                  |
| People Ops Coordinator   | HR, Projects, CRM                                                           |
| Operations Coordinator   | Assets, Support, Quality, Website, Regional Compliance, Reporting Analytics |

## Change Pipeline Gate Policy

1. Gate 1 (Reviewer): FAIL on any Critical/High finding → return to Frappe Customizer. Strict. No bypass.
2. Gate 2 (QA Tester): FAIL on any test failure → return to Frappe Customizer. Strict. No bypass.
3. RETRY_COUNT >= 2 on any gate → halt pipeline and escalate to user.
4. NEEDS-REVIEW (Medium/Low findings only) → advance with findings attached.

## Codebase-First Baseline

1. Mutation requests require discovery of existing DocType/hooks/service touchpoints before implementation.
2. Agents should extend current module behavior, not build parallel systems.
3. Outputs must include reuse evidence (what existing behavior was integrated).

## Safety Baseline

1. Never modify Frappe/ERPNext core.
2. MCP-first for ERPNext operations, bench fallback only when unsupported/unavailable.
3. Production-style contexts require explicit user confirmation for mutating steps.
4. Every mutating step must include a verification step.
