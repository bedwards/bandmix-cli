"""CLI entry point for bandmix-cli."""

import click

from bandmix_cli import __version__


@click.group()
@click.version_option(version=__version__)
def cli():
    """bandmix-cli — CLI tool for BandMix.com."""


def main():
    cli()


if __name__ == "__main__":
    main()
