# -*- coding: utf-8 -*-

"""Main code."""

from pathlib import Path
from typing import Iterable, List, Optional

from pyobo import Obo, Reference, SynonymTypeDef, Term, TypeDef

from debio.resources import PROPERTIES, TERMS, TYPEDEFS
from debio.version import VERSION

__all__ = [
    "DecentralizedBiomedicalOntology",
]

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.parent.resolve()
DOCS = ROOT.joinpath("docs")

PREFIX = "debio"
URI_PREFIX = "https//biopragmatics.github.io/debio/"
IDSPACES = {
    PREFIX: URI_PREFIX,
    "RO": "http://purl.obolibrary.org/obo/RO_",
}


def get_typedefs() -> Iterable[TypeDef]:
    """Get type definitions and properties."""
    for typedef in TYPEDEFS:
        yield _get_typedef(typedef)
    for prop in PROPERTIES:
        yield _get_typedef(prop, is_metadata_tag=True)


def _get_typedef(typedef, is_metadata_tag: Optional[bool] = None) -> TypeDef:
    return TypeDef(
        reference=Reference(
            prefix=PREFIX,
            identifier=typedef["identifier"],
            name=typedef["name"],
        ),
        definition=typedef.get("description"),
        holds_over_chain=[
            Reference(
                prefix=reference["prefix"],
                identifier=reference["identifier"],
                name=reference["name"],
            )
            for reference in typedef.get("holds_over_chain", [])
        ],
        is_metadata_tag=is_metadata_tag,
        xrefs=[
            Reference(prefix=xref["prefix"], identifier=xref["identifier"], name=xref.get("name"))
            for xref in typedef.get("xrefs", [])
        ],
    )


def get_synonyms() -> List[SynonymTypeDef]:
    """Get synonym type definitions."""
    return []


def get_terms() -> Iterable[Term]:
    """Get terms."""
    for term in TERMS:
        yield _get_term(term)


def _get_term(term) -> Term:
    pass


class DecentralizedBiomedicalOntology(Obo):
    """Get the ontology."""

    ontology = PREFIX
    typedefs = list(get_typedefs())
    synonym_typedefs = list(get_synonyms())
    idspaces = IDSPACES

    def iter_terms(self, force: bool = False) -> Iterable[Term]:
        """Iterate over terms in the ontology."""
        return get_terms()

    def _get_version(self) -> str:
        return VERSION


def _write(ontology: Obo, directory: Path):
    from bioontologies.robot import convert, convert_to_obograph

    directory.mkdir(exist_ok=True, parents=True)
    stub = directory.joinpath(ontology.ontology)
    obo_path = stub.with_suffix(".obo")
    ontology.write_obo(obo_path)
    convert_to_obograph(input_path=obo_path, json_path=stub.with_suffix(".json"))
    convert(input_path=obo_path, output_path=stub.with_suffix(".owl"))


def _main():
    from pyobo.ssg import make_site

    ontology = DecentralizedBiomedicalOntology()
    make_site(ontology, DOCS, manifest=True)

    current = ROOT.joinpath("releases", "current")
    _write(ontology, current)
    if not ontology.data_version.endswith("-dev"):
        release = ROOT.joinpath("releases", ontology.data_version.removesuffix("-dev"))
        _write(ontology, release)


if __name__ == "__main__":
    _main()
