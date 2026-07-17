---
name: frappe-docker-bench-ops
description: "Command-first frappe_docker operations. Use for bench execute, migrations, cache clear, site checks, and troubleshooting in Dockerized ERPNext. Keywords: docker exec bench, bench migrate, clear-cache, site troubleshooting."
argument-hint: "Provide site name, command objective, and whether changes are read-only or state-changing"
user-invocable: true
---

# Frappe Docker Bench Operations

## When To Use

- Running bench commands inside frappe_docker containers
- Diagnosing site-level issues
- Verifying post-change behavior with direct commands

## Procedure

1. Identify target container and site.
2. Prefer read-only checks first.
3. In production-like contexts, request explicit confirmation before state-changing commands.
4. Run explicit docker exec + bench command.
5. Capture output and summarize key evidence.
6. If state-changing command was run, perform a verification command immediately.

## Command Style

- Always provide copy-pasteable commands.
- Include site explicitly: bench --site <site>
- Keep one command per step with expected result notes.

## Expected Output

- Command sequence
- Key output highlights
- Verified outcome
- Safe next command
