---
name: format-code-style
description: Use this skill when writing, editing, reviewing, or formatting code to match the user's personal coding style, especially around documentation, comments, naming, code shape, Python typing, Ruff, and compact readable model code.
---

# Format Code Style

Use this skill for code generation, editing, review, and formatting when the user wants code to match their personal style.

## Workflow

1. Inspect the current project style before editing. If the project has an established convention that conflicts with this skill, mention the conflict and prefer the project convention unless the user asks otherwise.
2. Read `references/style.md` before non-trivial coding, editing, or review work. Use it to guide documentation, comments, naming, code shape, typing, interfaces, tests, and scripts.
3. Make the requested code changes while preserving behavior. Do not introduce refactors just to satisfy style preferences.
4. Use Ruff for Python formatting and lint rules it can handle reliably.
5. Finish Python work by running the bundled Ruff scripts when the environment allows it. Read `references/ruff.md` for script details.

## Core Preferences

- Keep code readable, clean, and locally understandable without adding ceremony.
- Trust type annotations by default; avoid extra runtime checks unless inputs cross a real boundary.
- Prefer compact, continuous code when it remains easy to read; split helpers only when they clarify a real concept or repeated logic.
- Use comments and docstrings to explain intent, responsibility, and workflow, not obvious code.
- Keep project conventions first. Use this skill to fill gaps or resolve ambiguity.

For detailed preferences, read `references/style.md`.

## Scripts

The bundled scripts run against the caller's current project directory:

```bash
scripts/ruff_check.sh [paths...]
scripts/ruff_format.sh [paths...]
scripts/ruff_fix.sh [paths...]
```

If no path is passed, each script targets `.`.
If the project has no Ruff configuration, scripts use `assets/ruff.toml` as a fallback without writing configuration into the project.

For Python Ruff behavior and scripts, read `references/ruff.md`.