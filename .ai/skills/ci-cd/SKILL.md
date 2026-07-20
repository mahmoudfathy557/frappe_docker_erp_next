# CI/CD — frappe_docker

GitHub Actions workflows for build, test, and release.

## Workflow Summary

| File | Trigger | Purpose |
|---|---|---|
| `build_stable.yml` | Tag push (`v*`) | Build & push stable images |
| `build_develop.yml` | Push to develop | Build develop images |
| `core-build-stable.yml` | Frappe/ERPNext release | Rebuild stable images on upstream release |
| `core-build-develop.yml` | Scheduled / push | Develop branch images |
| `core-publish-images.yml` | Manual | Publish multi-arch images |
| `app-build-image.yml` | Manual / push | Build custom app images |
| `docs-publish-site.yml` | Push to main | Deploy VitePress docs to Pages |
| `lint.yml` | PR / push | pre-commit + shellcheck |
| `pre-commit-autoupdate.yml` | Monthly | Auto-update pre-commit hooks |
| `stale.yml` | Daily | Close stale issues |

## Docker Buildx Bake

Images built via `docker-bake.hcl`:

```bash
# Build all targets
docker buildx bake

# Specific target
docker buildx bake bench

# Multi-arch
docker buildx bake --set *.platform=linux/amd64,linux/arm64
```

Key variables: `FRAPPE_VERSION`, `ERPNEXT_VERSION`, `PYTHON_VERSION`, `NODE_VERSION`, `REGISTRY_USER`.

## Custom App Image Workflow

`app-build-image.yml` — called from external repos via workflow dispatch:

```yaml
jobs:
  build:
    with:
      app_name: crm
      app_repo: acme/crm
      image_name: ghcr.io/acme/crm
```

Outputs a ready-to-use image with the app pre-installed. See `docs/08-reference/06-github-actions-image-workflows.md`.

## Pre-commit

Configured in `.pre-commit-config.yaml`:
- `pre-commit-hooks` — shebang, whitespace, EOF
- `pyupgrade` — Python syntax modernization
- `black` — Python formatting
- `isort` — Python import sorting
- `prettier` — JS/YAML/MD formatting (excludes `pnpm-lock.yaml`)
- `codespell` — spelling check
- `shfmt` — shell formatting (local, golang)
- `shellcheck` — shell linting

Run: `pre-commit run --all-files`
