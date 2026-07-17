# ERPNext Module Coverage Ledger

This ledger tracks operational completeness for module workflows.

| Module | Status | Preferred Path | Fallback Path | Notes |
| --- | --- | --- | --- | --- |
| Accounts | MCP+Fallback | ERPNext MCP | docker exec + bench | Validate fiscal year/period constraints |
| Selling | MCP+Fallback | ERPNext MCP | docker exec + bench | Include submit/cancel guardrails |
| Buying | MCP+Fallback | ERPNext MCP | docker exec + bench | Validate supplier and taxes |
| Stock | MCP+Fallback | ERPNext MCP | docker exec + bench | Verify warehouses and bins |
| Manufacturing | MCP+Fallback | ERPNext MCP | docker exec + bench | Validate BOM and Work Order lifecycle |
| HR | MCP+Fallback | ERPNext MCP | docker exec + bench | Permissions and payroll constraints |
| Projects | MCP+Fallback | ERPNext MCP | docker exec + bench | Task/project state validation |
| CRM | MCP+Fallback | ERPNext MCP | docker exec + bench | Lead/opportunity conversion checks |
| Assets | MCP+Fallback | ERPNext MCP | docker exec + bench | Asset lifecycle verification |
| Support | MCP+Fallback | ERPNext MCP | docker exec + bench | Issue/status transitions |
| Quality | MCP+Fallback | ERPNext MCP | docker exec + bench | Inspection links and statuses |
| Website | Fallback-Only | bench/app code | docker exec + bench | Often customization-heavy |
| Regional/Compliance | Mixed | ERPNext MCP where available | docker exec + bench | Country-specific validations |
| Reporting/Analytics | MCP+Fallback | ERPNext MCP | docker exec + bench | Read-heavy, low mutation risk |

## Status Legend

1. MCP-Only
2. MCP+Fallback
3. Fallback-Only
4. Blocked
