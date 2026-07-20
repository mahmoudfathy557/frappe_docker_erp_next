# Frappe Development — frappe_docker

Bench CLI, app lifecycle, site management, and debugging patterns.

## Development Setup

### DevContainer (Recommended)
```bash
cp -R devcontainer-example .devcontainer
# VSCode: Reopen in Container → python installer.py
```

### Manual Inside Container
```bash
cd /workspace/development
python installer.py  # interactive prompts
bench start          # hot-reload on :8000
```

## Bench Commands

### Apps
| Command | Purpose |
|---|---|
| `bench new-app <name>` | Create new app |
| `bench get-app <git_url>` | Download app |
| `bench --site <site> install-app <name>` | Install to site |
| `bench --site <site> list-apps` | List installed |
| `bench build --app <name>` | Build frontend assets |

### Sites
| Command | Purpose |
|---|---|
| `bench new-site <name>` | Create site |
| `bench --site <name> console` | Python REPL with Frappe context |
| `bench --site <name> migrate` | Run migrations |
| `bench --site all backup --with-files` | Backup all sites |

### Container Access
```bash
docker compose -f pwd.yml exec backend bash
docker compose -f pwd.yml cp backend:/home/frappe/frappe-bench/apps/ ./local-apps/
docker compose -f pwd.yml logs -f backend
```

## Custom App Structure
```
my_app/
├── hooks.py              # Lifecycle hooks
├── modules.txt           # Module list
├── my_app/
│   ├── config/desktop.py # Workspace icons
│   ├── doctype/<name>/   # DocType + controller
│   ├── page/             # Custom pages
│   └── public/           # Static assets
├── templates/            # Jinja2 templates
├── www/                  # Web routes
└── requirements.txt
```

## Key Debugging
- `bench console` — Python REPL
- `bench mariadb` — DB console
- `bench clear-cache` — Redis cache flush
- Logs: `development/frappe-bench/logs/`

## Custom App Boundary

Core modules are **READ-ONLY**. Never modify:

| Directory | Rule |
|---|---|
| `apps/frappe/` | Read-only — core framework |
| `apps/erpnext/` | Read-only — core ERP |
| `apps/hrms/` | Read-only — official app |
| Any official app | Read-only |

To extend behavior:

1. **Use configuration first** — custom fields, workflows, permissions, print formats, email templates (no code)
2. **Use DocType extension** — `custom:` fields via the UI or `frappe.custom_field` in a custom app
3. **Use hooks.py** — in your custom app, hook into core DocType events (`validate`, `on_update`, etc.)
4. **Create new DocTypes** — only when no existing DocType suffices

All custom code lives in a `bench new-app` created app, never in core modules.

## Version Branches
- Frappe & ERPNext must match: `version-14` with `version-14`
- `bench get-app --branch version-14 --resolve-deps erpnext`
