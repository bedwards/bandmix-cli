# bandmix-cli

A command-line tool for reading and writing data on [BandMix.com](https://www.bandmix.com). The site has no public API, so the CLI operates via authenticated HTTP requests, scraping HTML responses and submitting standard form POSTs.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Quickstart

```bash
uv sync --all-groups
bandmix auth login --email you@example.com
bandmix search --instruments Drums --genre Country --radius 50
```

## Features

- **Authentication** — Session-based login with cookie persistence
- **Profile** — Read and update your BandMix profile
- **Search** — Find musicians and bands with filters (instrument, genre, location, etc.)
- **Member** — View any member's public profile
- **Messages** — Read and send messages (Premier membership required for sending)
- **Feed** — View activity feed
- **Photos / Music / Videos** — Manage media uploads
- **Calendar** — Manage gig calendar
- **Seeking** — Manage "Now Seeking" ads
- **Music List** — Manage bookmarked profiles
- **Settings** — Email, match mailer, dashboard options

## Development

```bash
uv sync --all-groups
uv run pytest
uv run ruff check
uv run ruff format --check
uv run pre-commit install
```

## CI

GitHub Actions runs lint, format check, and tests on every push and PR to `main`.

## License

Unlicensed.
