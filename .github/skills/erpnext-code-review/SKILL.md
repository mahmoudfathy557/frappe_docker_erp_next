---
name: erpnext-code-review
description: "Structured code review for Frappe/ERPNext custom app files. Use when auditing hook placement, API usage, security risks, and test presence before merging changes. Keywords: review code, audit hooks, check API, OWASP, anti-pattern, code quality, pre-merge."
argument-hint: "Provide the file path(s) or diff to review, plus a brief description of the change intent"
user-invocable: true
---

# ERPNext Code Review

## When To Use

- Reviewing changed files in a custom app before merge
- Auditing hook placement and API call safety
- Checking OWASP risk surface of server-side Frappe code
- Verifying test coverage for a new feature or bug fix

## Procedure

1. Read the changed files (or diff).
2. Build a short reuse map: existing touchpoints used vs new logic introduced.
3. Run each checklist section below in order.
4. Record every finding with file, line, severity, and description.
5. Produce the final verdict and delegation instructions.

## Checklist

### 1. Hook Correctness

- [ ] `before_save` used only for pre-persistence normalization or validation
- [ ] `after_insert` used only for side effects requiring a persisted record
- [ ] `on_submit` used only for finalization-locked state actions
- [ ] `validate` used for user-facing validation errors via `frappe.throw`
- [ ] No business logic placed in hooks that run on every page load (`on_load`, `onload`)

### 2. API Safety

- [ ] No `frappe.db.sql` with `.format()` or f-string interpolation
- [ ] `frappe.db.sql` only used when necessary and always with `%s` parameterization
- [ ] No direct `pymysql` / `psycopg2` imports
- [ ] Allowed APIs only: `frappe.db.get_value`, `frappe.get_doc`, `frappe.get_list`, `frappe.db.set_value`, `frappe.db.exists`
- [ ] No hardcoded credentials, API keys, or site names

### 3. Core Isolation

- [ ] All changed files are under `apps/<custom_app>/`
- [ ] No patches or monkey-patches targeting `frappe.*` or `erpnext.*` modules

### 4. OWASP Checks (Server-Side Frappe)

- [ ] **A01 Broken Access Control** — `frappe.has_permission()` called before sensitive reads or writes
- [ ] **A03 Injection** — no unparameterized SQL; no `eval` / `exec` on user-controlled input
- [ ] **A05 Security Misconfiguration** — no committed debug flags; no internal endpoints exposed without auth
- [ ] **A09 Logging & Monitoring** — no bare `except: pass`; failures logged with `frappe.log_error`

### 5. Test Coverage

- [ ] A unit test exists covering the changed logic path
- [ ] Tests extend `FrappeTestCase` or `unittest.TestCase`
- [ ] Tests are isolated — no dependence on live external services or hardcoded production data
- [ ] Tests are discoverable under `tests/test_*.py` in the module directory

### 6. Integration and Reuse

- [ ] Existing DocType/services/hooks are reused where possible
- [ ] New abstractions are justified and scoped to the gap only
- [ ] No duplicate parallel workflow introduced for an existing ERPNext module

## Output Format

| File            | Line | Severity | Category   | Finding                                           |
| --------------- | ---- | -------- | ---------- | ------------------------------------------------- |
| path/to/file.py | 42   | High     | API Safety | frappe.db.sql with f-string interpolation         |
| path/to/file.py | 87   | Medium   | Hook       | Business logic in on_load runs on every page view |

**Severity scale:** Critical > High > Medium > Low > Info

**Verdict:** PASS / FAIL / NEEDS-REVIEW

**Delegation:**

- Fixes → Frappe Customizer
- Test gaps → ERPNext QA Tester
