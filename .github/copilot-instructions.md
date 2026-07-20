# frappe_docker — AI Project Context

## Architecture

Multi-service Docker deployment for Frappe/ERPNext. Core services: configurator, backend (Werkzeug), frontend (Nginx), websocket (Socket.IO), queue-short/long (RQ workers), scheduler. Optional: MariaDB/Postgres, Redis, Traefik/nginx-proxy.

## Key Conventions

- **Compose overrides** over editing `compose.yaml` directly. Override files live in `overrides/`.
- **Images**: 4 types — `bench/` (CLI only), `custom/` (production, configurable via apps.json), `layered/` (prebuilt deps), `production/` (quick start).
- **Builds**: Docker Buildx Bake via `docker-bake.hcl`.
- **Commits**: Conventional Commits per `CONTRIBUTING.md`.
- **Pre-commit**: `.pre-commit-config.yaml` — run `pre-commit run --all-files`.

## Agent Framework

`.ai/` directory contains agents (7-role orchestrated SDLC), skills (6 domains), MCP servers, and hooks. See `.ai/README.md`.
