# Consignment Deployment Readiness Healthcheck

Use this healthcheck before enabling or promoting consignment customizations across environments.

## Bench Execute Commands

Run readiness check:

```bash
bench --site <site-name> execute client_customizations.consignment.services.readiness.run_consignment_readiness_healthcheck
```

Pretty-print output in shell (optional):

```bash
bench --site <site-name> execute client_customizations.consignment.services.readiness.run_consignment_readiness_healthcheck | jq
```

## Output Shape

The command returns a structured payload:

- overall_status: PASS, WARN, or FAIL
- checks: list of readiness checks
  - name
  - status
  - details
  - missing_items (when relevant)

Example (abbreviated):

```json
{
  "overall_status": "FAIL",
  "checks": [
    {
      "name": "required_doctypes",
      "status": "PASS",
      "details": "Consignment custom DocType presence",
      "missing_items": []
    },
    {
      "name": "required_custom_fields",
      "status": "FAIL",
      "details": "Consignment custom field presence",
      "missing_items": [
        "Delivery Note Item-custom_consignment_settlement"
      ]
    }
  ]
}
```

## Interpretation Guidance

- PASS: Required consignment metadata and hook configuration checks all passed.
- WARN: Non-blocking concern detected. Review details before deployment.
- FAIL: Blocking readiness gaps detected. Resolve all missing items and re-run.

## What Is Checked

- Required custom DocTypes:
  - Consignment Agreement
  - Consignment Agreement Item
  - Consignment Settlement
  - Consignment Settlement Item
- Required Custom Field records used by the consignment flow.
- Deterministic hook configuration check against expected `doc_events` and `scheduler_events` values in app hooks.

## Notes

- Hook verification is deterministic config validation from app hooks constants and does not rely on complex runtime hook introspection.
- This healthcheck does not mutate data.
