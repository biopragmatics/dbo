"""CLI for DeBiO."""

import click

from debio import DecentralizedBiomedicalOntology
from debio.api import DOCS, ROOT, write

__all__ = [
    "main",
]


@click.group()
def main():
    """Run the DeBiO CLI."""


@main.command()
def export():
    """Export the data."""
    from pyobo.ssg import make_site

    ontology = DecentralizedBiomedicalOntology()
    make_site(ontology, DOCS, manifest=True)

    current = ROOT.joinpath("releases", "current")
    write(ontology, current)
    if not ontology.data_version.endswith("-dev"):
        release = ROOT.joinpath("releases", ontology.data_version)
        write(ontology, release)


if __name__ == "__main__":
    main()
