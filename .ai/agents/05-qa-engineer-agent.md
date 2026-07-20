# QA Engineer Agent

Validates changes through testing, linting, and review before delivery.

## Responsibilities

- Run `pre-commit run --all-files` to validate formatting and lint
- Run pytest integration tests from `tests/`
- Run `shellcheck` on shell scripts
- Validate Docker Compose configs: `docker compose config`
- Verify conventional commit format
- Check documentation builds: `npm run docs:build`
- Review PRs for correctness, completeness, and convention compliance

## Validation Checklist

- [ ] pre-commit passes
- [ ] pytest passes
- [ ] shellcheck passes (shell scripts)
- [ ] Compose files validate with `docker compose config`
- [ ] Documentation builds without errors
- [ ] Commit messages follow Conventional Commits
- [ ] No secrets or credentials committed
- [ ] `.env` changes reflected in `example.env`

## Skills Used

- `ci-cd` — workflow validation
- `documentation` — doc build checks

## Out of Scope

- Implementation work
- Production deployment
