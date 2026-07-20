# Docker Patterns — frappe_docker

Multi-service Docker architecture for Frappe/ERPNext.

## Compose Architecture

`compose.yaml` defines core services. All extensions go in `overrides/compose.*.yaml`.

### Core Services
| Service | Role |
|---|---|
| `configurator` | One-shot init — sets DB/Redis config, exits |
| `backend` | Werkzeug WSGI server |
| `frontend` | Nginx reverse proxy + static assets |
| `websocket` | Socket.IO real-time (Node.js) |
| `queue-short` / `queue-long` | RQ background workers |
| `scheduler` | Cron-style scheduled tasks |

### Override Files
| Override | Adds |
|---|---|
| `compose.mariadb.yaml` | MariaDB database |
| `compose.postgres.yaml` | PostgreSQL database |
| `compose.redis.yaml` | Redis cache + queue |
| `compose.proxy.yaml` | Traefik reverse proxy |
| `compose.https.yaml` | Traefik + Let's Encrypt |
| `compose.nginxproxy.yaml` | nginx-proxy (HTTP) |
| `compose.nginxproxy-ssl.yaml` | nginx-proxy + acme-companion (HTTPS) |

### Running
```bash
docker compose -f compose.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.redis.yaml up -d
```

## Image Types

| Directory | Base | Customizable | Use Case |
|---|---|---|---|
| `images/bench/` | Debian | No | CLI-only, debugging |
| `images/custom/` | Python slim | Yes (apps.json) | Production, controlled versions |
| `images/layered/` | Prebuilt Hub | Yes (apps.json) | Fast production builds |
| `images/production/` | Debian | No | Quick start, exploration |

## Multi-Arch Builds

```bash
docker buildx bake --set *.platform=linux/amd64,linux/arm64
```

Key vars in `docker-bake.hcl`: `PYTHON_VERSION`, `NODE_VERSION`, `FRAPPE_VERSION`, `ERPNEXT_VERSION`.

## Bind Mounts

| Flag | Use |
|---|---|
| `:cached` | macOS/Windows — host writes buffered |
| `:delegated` | Container writes heavily |
| `:consistent` | Full sync (slow) |

## Quick Test (pwd.yml)

```bash
docker compose -f pwd.yml up -d
# http://localhost:8080 | Administrator / admin
```
