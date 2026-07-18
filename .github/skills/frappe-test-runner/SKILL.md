---
name: frappe-test-runner
description: "Execute Frappe/ERPNext Python unit tests inside the Docker bench environment. Use when running tests, diagnosing failures, or validating custom app logic after a change. Keywords: unittest, run tests, test failure, bench test, python -m unittest, discover tests."
argument-hint: "Specify the app name, module path, and optionally a test class or method to target"
user-invocable: true
---

# Frappe Test Runner

## When To Use

- Running unit tests for a custom app after a code change
- Verifying a fix resolves a failing test
- Checking test output after a new customization is deployed

## Container Name Resolution

Identify the backend container first:

```powershell
docker ps --filter "name=backend" --format "{{.Names}}"
```

Use the returned name in place of `<container>` below.

## Command Patterns

### Discover and run all tests in a module directory

```bash
docker exec <container> \
  python -m unittest discover \
  -s apps/<app_name>/<app_name>/<module>/tests \
  -p "test_*.py" -v
```

### Run a single test file

```bash
docker exec <container> \
  python -m unittest \
  apps.<app_name>.<module>.tests.<test_module> -v
```

### Run a single test class

```bash
docker exec <container> \
  python -m unittest \
  apps.<app_name>.<module>.tests.<test_module>.<TestClass> -v
```

### Run a single test method

```bash
docker exec <container> \
  python -m unittest \
  apps.<app_name>.<module>.tests.<test_module>.<TestClass>.<test_method> -v
```

## Procedure

1. Resolve the container name.
2. Identify the target test path from the failing output or the changed source file.
3. Run the narrowest targeted command first (method > class > module > discover).
4. Capture stdout and stderr in full.
5. Parse output for `FAIL`, `ERROR`, and `OK` lines.
6. For each failure, extract: test name, AssertionError message, traceback file and line.
7. Map traceback paths back to custom app source files.
8. Report counts and findings.

## Escalation Rule

Only run full-suite discover if the targeted run cannot isolate the failure.

## Expected Output

- Command used (copy-pasteable)
- Pass/fail/error counts
- Per-failure: test name | assertion message | source file:line
- Suggested next action
