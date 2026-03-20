# GEMINI.md

Instructions for Gemini when working in this repository.

## Project overview

**bandmix-cli** is a Python 3.13 CLI tool for BandMix.com, managed with **uv** and built with **hatchling**. The package source lives in `src/bandmix_cli/`.

## Key commands

```bash
uv sync --all-groups        # Install all dependencies (dev + local)
uv run pytest               # Run tests
uv run ruff check           # Lint
uv run ruff format --check  # Check formatting
uv run pre-commit run --all-files  # Run all pre-commit hooks
uv run bandmix              # Run the CLI
```

## Architecture

- **Package**: `src/bandmix_cli/` — the installable package.
  - `main.py` — Click CLI entry point (registered as `bandmix` in `pyproject.toml`).
  - `auth.py` — Login, session persistence, session validation.
  - `client.py` — HTTP client (requests.Session wrapper, cookie jar).
  - `parser.py` — BeautifulSoup HTML parsers, one per page type.
  - `models.py` — Pydantic models for all data entities.
  - `enums.py` — Instrument, Genre, State, Commitment enums.
  - `formatters.py` — table/json/text output renderers.
  - `commands/` — Click command groups (profile, search, member, etc.).
- **Tests**: `tests/` — uses pytest. Import from `bandmix_cli` directly.
- **Scripts**: `scripts/clean.py` — utility to remove build artifacts.
- **CI**: `.github/workflows/ci.yml` — GitHub Actions runs ruff check, ruff format, and pytest on Python 3.13 / ubuntu-latest.

## Conventions

- Use **ruff** for linting and formatting (no black/isort/flake8).
- Pre-commit hooks enforce ruff check, ruff format, and pytest before every commit.
- All source code is in `src/` layout.
- Tests import from the installed package, not relative paths.
- Commit messages should be concise and descriptive.
