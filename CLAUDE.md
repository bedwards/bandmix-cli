# CLAUDE.md

Instructions for Claude Code when working in this repository.

## Project overview

**tlon-uqbar** is a Python 3.13 project managed with **uv** and built with **hatchling**. The package source lives in `src/tlon_uqbar/`.

## Key commands

```bash
uv sync --all-groups        # Install all dependencies (dev + local)
uv run pytest               # Run tests
uv run ruff check           # Lint
uv run ruff format --check  # Check formatting
uv run pre-commit run --all-files  # Run all pre-commit hooks
```

## Architecture

- **Package**: `src/tlon_uqbar/` — the installable package. `__init__.py` exports `message`. `main.py` is the CLI entry point (registered as `main` in `pyproject.toml`).
- **Tests**: `tests/test_core.py` — uses pytest. Import from `tlon_uqbar` directly.
- **Scripts**: `scripts/clean.py` — utility to remove `__pycache__`, `.pytest_cache`, `.ruff_cache`, `dist`, and `build` directories.
- **CI**: `.github/workflows/ci.yml` — GitHub Actions runs ruff check, ruff format, and pytest on Python 3.13 / ubuntu-latest.

## Conventions

- Use **ruff** for linting and formatting (no black/isort/flake8).
- Pre-commit hooks enforce ruff check, ruff format, and pytest before every commit.
- All source code is in `src/` layout.
- Tests import from the installed package, not relative paths.
- Commit messages should be concise and descriptive.

## Dependency management

- Runtime deps go in `[project] dependencies`.
- Dev tools (pytest, ruff, pre-commit) go in `[dependency-groups] dev`.
- Local/interactive tools (ipython) go in `[dependency-groups] local`.
- Always use `uv sync --all-groups` to install everything.
