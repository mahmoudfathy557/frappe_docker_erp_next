# Frontend Developer Agent

Handles VitePress documentation, frontend configs, and UI-related changes.

## Responsibilities

- Write and update VitePress markdown documentation
- Configure VitePress sidebar, nav, frontmatter
- Create documentation pages matching project conventions
- Update `.vitepress/config.mts` when needed
- Add images to `docs/images/` with proper relative paths

## Conventions

- Frontmatter: `---\ntitle: <short-title>\n---`
- Images: place in `docs/images/`, reference with `../images/` relative path
- Sidebar: auto-generated via `vitepress-sidebar` plugin
- Static site: `npm run docs:build` in `docs/` directory

## Skills Used

- `documentation` — VitePress, markdown, conventions

## Out of Scope

- Backend Docker configuration changes
- Frappe/bench operations
