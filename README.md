# Tlön, Uqbar

A Python project scaffold with modern tooling.

> *"Tlön, Uqbar, Orbis Tertius"* — Jorge Luis Borges

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Quickstart

```bash
uv sync --all-groups
uv run main
```

## Development

### Install dependencies

```bash
uv sync --all-groups
```

### Run tests

```bash
uv run pytest
```

### Lint & format

```bash
uv run ruff check
uv run ruff format --check
```

### Pre-commit hooks

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

### Clean build artifacts

```bash
python scripts/clean.py
```

## CI

GitHub Actions runs lint, format check, and tests on every push and PR to `main`. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Project structure

```
src/tlon_uqbar/       # Package source
  __init__.py          # Exports `message`
  main.py              # CLI entry point
scripts/
  clean.py             # Remove __pycache__, .pytest_cache, etc.
tests/
  test_core.py         # Core tests
```

## License

Unlicensed.
