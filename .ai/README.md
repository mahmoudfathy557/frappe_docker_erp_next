# frappe_docker AI Framework

Orchestrator-led SDLC agent hierarchy for the Frappe Docker project.

## Architecture

```
User Request
    ↓
[00-Orchestrator]  ←─ routes to specialist
    ↓
[01-PM] → [02-Architect] → [03-Frontend | 04-Backend] → [05-QA] → [06-DevOps]
```

Each agent hands off context to the next. No stage is skipped for delivery work.

## Structure

| Directory | Contents |
|---|---|
| `.ai/agents/` | 7 agent definitions (numbered for orchestration order) |
| `.ai/skills/` | 6 domain-specific skill packs |
| `.ai/mcps/` | MCP server configuration |
| `.ai/hooks/` | Git hooks with AI-aware validation |

## Skills

| Skill | Domain | Source |
|---|---|---|
| `docker-patterns` | Compose, Bake, images, overrides, multi-arch | `compose.yaml`, `docker-bake.hcl`, `overrides/` |
| `frappe-development` | Bench, apps, sites, doctypes, debugging | `docs/05-development/`, `docs/09-concepts/` |
| `erpnext-business` | ERPNext modules, workflows, company setup | `docs.frappe.io/erpnext/` |
| `documentation` | VitePress, frontmatter, markdown | `docs/.vitepress/`, `CONTRIBUTING.md` |
| `ci-cd` | GitHub Actions, image builds, releases | `.github/workflows/` |
| `migration` | Version bumps, Traefik v3, Postgres upgrade | `docs/06-migration/` |

## Hooks

| Hook | Purpose |
|---|---|
| `pre-commit` | Project standards + AI-aware validation |
| `pre-push` | Full lint + test before push |
| `commit-msg` | Conventional commit enforcement |

## Platform Support

- **opencode**: configured via `opencode.json`
- **GitHub Copilot**: configured via `.github/copilot-instructions.md`
