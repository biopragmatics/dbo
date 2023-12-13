"""CLI for DeBiO."""

import click

from debio.api import export

__all__ = [
    "main",
]


@click.group()
def main():
    """Run the DeBiO CLI."""


main.add_command(export)


if __name__ == "__main__":
    main()
