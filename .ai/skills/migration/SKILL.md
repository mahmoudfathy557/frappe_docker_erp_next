# Migration — frappe_docker

Version upgrades, database migration, and infrastructure changes.

## Frappe/ERPNext Version Bumps

When a new Frappe/ERPNext release triggers image rebuilds:

1. Update `ERPNEXT_VERSION` in `example.env`
2. Update `FRAPPE_VERSION` and `ERPNEXT_VERSION` in `docker-bake.hcl`
3. CI workflows auto-build on tag push (`.github/workflows/build_stable.yml`)
4. Stable builds publish to Docker Hub as `frappe/erpnext`

## Debian Release Migration

When Debian moves (e.g., bullseye → bookworm):

| File | Changes |
|---|---|
| `images/erpnext/Containerfile` | Base image tag, Python version, apt packages, wkhtmltopdf |
| `images/custom/Containerfile` | Same as above |
| `images/bench/Dockerfile` | Base image tag, apt packages, wkhtmltopdf |

## Traefik v2 → v3 Migration

See `docs/06-migration/02-traefik-v3-migration.md`:
- Router/Service/Middleware label syntax changes
- `stripPrefix` → `stripPrefixRegex` migration
- TLS configuration updates

## PostgreSQL Major Version Upgrade

See `docs/06-migration/03-postgres-major-version-upgrade.md`:
- Dump old DB → install new Postgres → restore
- Update `DB_HOST`/`DB_PORT` in env
- Test app compatibility

## Multi-Image → Single-Image Migration

For users migrating from the old multi-image setup (`images/v12/` era):

See `docs/06-migration/01-migrate-from-multi-image-setup.md`:
- New image structure (`custom/`, `layered/`, `production/`)
- Compose override patterns
- apps.json configuration for custom apps

## General Upgrade Checklist

- [ ] Backup DB and files before starting
- [ ] Test migration on staging first
- [ ] Update `example.env` version
- [ ] Update `docker-bake.hcl` version vars
- [ ] Check CI workflow version references
- [ ] Test compose config: `docker compose config`
- [ ] Run site migration: `bench --site all migrate`
- [ ] Verify functionality after migration
