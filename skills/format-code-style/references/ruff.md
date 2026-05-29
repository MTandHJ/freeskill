# Ruff Scripts

Use these scripts when a Python project needs formatting or basic Ruff checks.

## Commands

```bash
scripts/ruff_check.sh [paths...]
scripts/ruff_format.sh [paths...]
scripts/ruff_fix.sh [paths...]
```

- `ruff_check.sh`: runs `ruff check`, does not modify code.
- `ruff_format.sh`: runs `ruff format`.
- `ruff_fix.sh`: runs `ruff check --fix`, then `ruff format`.

If no path is passed, the target is `.`.

Examples:

```bash
scripts/ruff_check.sh
scripts/ruff_format.sh src tests
scripts/ruff_fix.sh src tests
```

## Configuration

The scripts do not create, overwrite, or edit project configuration.

Configuration behavior:

1. Search upward from the caller's current directory for `ruff.toml`, `.ruff.toml`, or a `pyproject.toml` containing `[tool.ruff]`.
2. If project configuration exists, use it.
3. If no project configuration exists, use the bundled fallback config at `assets/ruff.toml`.

The scripts require an existing `ruff` executable on `PATH`; they do not install dependencies.
