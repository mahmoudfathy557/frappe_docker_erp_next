# ERPNext Business Domain — frappe_docker

Business context for configuring and using ERPNext after Docker deployment.

## Reference Source

Primary: https://docs.frappe.io/erpnext/getting-started-with-erpnext

## Getting Started Workflow (from official docs)

1. **Define Needs** — Identify key modules needed (Accounting, Inventory, HR, CRM, Manufacturing)
2. **Choose Deployment** — Frappe Cloud (hosted) vs Self-hosted (this repo)
3. **Setup** (from Docker perspective): `docker compose up -d` → create site → install erpnext app
4. **Configure Basic Settings**:
   - Admin account creation
   - Company details (name, address, currency, fiscal year)
   - System configuration per module
5. **Train & Launch** — User training, go-live, monitoring

## Module Overview

| Module | Purpose | Docs Link |
|---|---|---|
| Accounting | Chart of Accounts, GL, AR/AP, Tax | https://docs.frappe.io/erpnext/user/manual/en/accounts |
| CRM | Leads, Opportunities, Customers | https://docs.frappe.io/erpnext/user/manual/en/CRM |
| HR | Employee, Payroll, Leave, Attendance | https://docs.frappe.io/erpnext/user/manual/en/human-resources |
| Selling | Quotations, Sales Orders, Customers | https://docs.frappe.io/erpnext/user/manual/en/selling |
| Buying | Purchase Orders, Suppliers | https://docs.frappe.io/erpnext/user/manual/en/buying |
| Stock | Items, Warehouses, Stock Entries | https://docs.frappe.io/erpnext/user/manual/en/stock |
| Manufacturing | BOM, Work Orders, Routing | https://docs.frappe.io/erpnext/user/manual/en/manufacturing |
| Assets | Fixed Assets, Depreciation | https://docs.frappe.io/erpnext/user/manual/en/asset |

## Business Workflows

### Quote-to-Cash
Lead → Opportunity → Quotation → Sales Order → Delivery Note → Sales Invoice → Payment

### Procure-to-Pay
Material Request → Purchase Order → Purchase Receipt → Purchase Invoice → Payment

## Module Interdependencies
- Stock Items must exist before Sales/Purchase transactions
- Chart of Accounts must be set up before Invoices
- Company must be created before any transaction
- Fiscal Year must be defined for accounting periods

## Key Configuration After Login
- `http://<your-site>/app/company` — Create your company
- `http://<your-site>/app/accounts-settings` — Accounting setup
- `http://<your-site>/app/stock-settings` — Inventory defaults
- `http://<your-site>/app/selling-settings` — Sales defaults
- `http://<your-site>/app/buying-settings` — Purchase defaults

## Check Before You Build

**Never create a custom app until you've verified the need isn't already covered.**

### Decision flow:

```
Business need
    ↓
Search existing ERPNext modules (table above)
    ├── Found → Configure it (settings, custom fields, workflows)
    │             ↓
    │            Use existing — no new app
    └── Not found → Check DocTypes via Desk (Setup → DocType List)
                      ├── Similar exists → Extend with custom fields + hooks
                      └── Nothing close → Create new custom app
```

### Built-in features to leverage first (no code needed):

| Feature | What it does |
|---|---|
| Custom Fields | Add fields to any DocType via UI |
| Workflows | State machines with approval steps |
| Permission Rules | Role-based access at row/field level |
| Print Formats | Custom PDF layouts (Jinja2) |
| Email Templates | Template-based automated emails |
| Report Builder | Custom reports without SQL |
| Web Form | Public-facing forms with DocType mapping |
| Custom DocType | New data models (but check first!) |

### When a custom app IS appropriate:

- New business domain not in ERPNext (e.g., a booking system for a niche industry)
- Integration with an external API that needs dedicated models
- Complex business logic that can't be expressed via workflows/scripts alone

## Extending Existing Modules (recommended path)

When building custom Frappe apps that extend ERPNext:

```python
# In your custom_app/hooks.py — hook into core DocType events
doc_events = {
    "Sales Invoice": {
        "on_submit": "your_app.api.on_sales_invoice_submit"
    }
}
```

- Use existing DocTypes as reference patterns
- Leverage built-in REST API (`/api/resource/<DocType>`)
- Use hooks.py for lifecycle integration without modifying core
- Follow existing module structure in `modules.txt`
