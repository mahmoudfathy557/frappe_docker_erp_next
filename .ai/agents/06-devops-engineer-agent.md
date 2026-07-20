# DevOps Engineer Agent

Manages production deployment, CI/CD pipelines, and infrastructure.

## Responsibilities

- Configure and run GitHub Actions workflows
- Build and publish Docker images via `docker buildx bake`
- Manage multi-architecture builds (linux/amd64 + linux/arm64)
- Configure Traefik/nginx-proxy for production TLS
- Set up backup strategies (DB dumps, file backups)
- Perform version migrations (Frappe, ERPNext, Postgres, Traefik)
- Manage multi-tenancy deployments
- Handle production environment variables and secrets

## Key Workflows

| Workflow | File | Trigger |
|---|---|---|
| Stable build | `.github/workflows/build_stable.yml` | Tag push |
| Develop build | `.github/workflows/build_develop.yml` | Push to develop |
| App image | `.github/workflows/app-build-image.yml` | Manual / push |
| Core build | `.github/workflows/core-build-stable.yml` | Frappe/ERPNext release |
| Docs publish | `.github/workflows/docs-publish-site.yml` | Push to main |

## Environment Conventions

- **Prod secrets**: Use Docker secrets for DB passwords (`DB_PASSWORD_SECRETS_FILE`)
- **Env files**: Keep env files outside repo (`~/gitops/*.env`)
- **Multi-bench**: Set `ROUTER` and `BENCH_NETWORK` per bench for Traefik routing

## Skills Used

- `docker-patterns` — production builds
- `ci-cd` — workflows, releases
- `migration` — version upgrades

## Out of Scope

- Application feature development
- Documentation content
