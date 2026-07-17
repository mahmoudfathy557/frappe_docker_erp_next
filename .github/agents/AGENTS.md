# Agent Registry

This registry is the source of truth for capability tiers, routing, and delegation contracts.

## Capability Tiers

1. Tier 0: Read-only analysis and routing
2. Tier 1: Safe write operations in development
3. Tier 2: State-changing ERPNext operations in development
4. Tier 3: Production-gated operations with explicit confirmation

## Agent Matrix

| Agent                          | Primary Scope                         | Tier Ceiling | Tools Profile               | Delegates To                                            |
| ------------------------------ | ------------------------------------- | ------------ | --------------------------- | ------------------------------------------------------- |
| ERPNext Orchestrator           | classification + delegation           | Tier 0       | read, search, agent         | ERPNext Operator, Frappe Customizer, module specialists |
| ERPNext Operator               | ERPNext document/data operations      | Tier 3       | read, search, execute       | none                                                    |
| Frappe Customizer              | custom app code changes and refactors | Tier 3       | read, search, edit, execute | none                                                    |
| Accounts Specialist            | Accounts workflows                    | Tier 3       | read, search, execute       | none                                                    |
| Selling Specialist             | Selling workflows                     | Tier 3       | read, search, execute       | none                                                    |
| Buying Specialist              | Buying workflows                      | Tier 3       | read, search, execute       | none                                                    |
| Stock Specialist               | Stock workflows                       | Tier 3       | read, search, execute       | none                                                    |
| Manufacturing Specialist       | Manufacturing workflows               | Tier 3       | read, search, execute       | none                                                    |
| HR Specialist                  | HR workflows                          | Tier 3       | read, search, execute       | none                                                    |
| Projects Specialist            | Projects workflows                    | Tier 3       | read, search, execute       | none                                                    |
| CRM Specialist                 | CRM workflows                         | Tier 3       | read, search, execute       | none                                                    |
| Assets Specialist              | Assets workflows                      | Tier 3       | read, search, execute       | none                                                    |
| Support Specialist             | Support workflows                     | Tier 3       | read, search, execute       | none                                                    |
| Quality Specialist             | Quality workflows                     | Tier 3       | read, search, execute       | none                                                    |
| Website Specialist             | Website workflows                     | Tier 3       | read, search, execute       | none                                                    |
| Regional Compliance Specialist | Regional/compliance workflows         | Tier 3       | read, search, execute       | none                                                    |
| Reporting Analytics Specialist | Reporting/analytics workflows         | Tier 3       | read, search, execute       | none                                                    |

## Deterministic Routing Rules

1. Data/document actions -> ERPNext Operator.
2. Code/hook/refactor actions -> Frappe Customizer.
3. Cross-cutting workflows -> Frappe Customizer then ERPNext Operator validation.
4. Unknown intent -> one clarification question, then route.

## Module Specialist Paths

1. Accounts -> Accounts Specialist
2. Selling -> Selling Specialist
3. Buying -> Buying Specialist
4. Stock -> Stock Specialist
5. Manufacturing -> Manufacturing Specialist
6. HR -> HR Specialist
7. Projects -> Projects Specialist
8. CRM -> CRM Specialist
9. Assets -> Assets Specialist
10. Support -> Support Specialist
11. Quality -> Quality Specialist
12. Website -> Website Specialist
13. Regional/Compliance -> Regional Compliance Specialist
14. Reporting/Analytics -> Reporting Analytics Specialist

## Safety Baseline

1. Never modify Frappe/ERPNext core.
2. MCP-first for ERPNext operations, bench fallback only when unsupported/unavailable.
3. Production-style contexts require explicit user confirmation for mutating steps.
4. Every mutating step must include a verification step.
