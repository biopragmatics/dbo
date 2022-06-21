# -*- coding: utf-8 -*-

"""Main code."""

from pathlib import Path
from typing import Iterable, List, Optional

from bioontologies.robot import convert, convert_to_obograph
from pyobo import Obo, Reference, SynonymTypeDef, Term, TypeDef
from pyobo.ssg import make_site

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
        holds_over_chain=[
            Reference(
                prefix=reference["prefix"],
                identifier=reference["identifier"],
                name=reference["name"],
            )
            for reference in typedef.get("holds_over_chain", [])
        ],
        is_metadata_tag=is_metadata_tag,
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


def _main():
    ontology = DecentralizedBiomedicalOntology()
    releases = ROOT.joinpath("releases", ontology.data_version.removesuffix("-dev"))
    releases.mkdir(parents=True, exist_ok=True)
    stub = releases.joinpath(ontology.ontology)
    obo_path = stub.with_suffix(".obo")
    ontology.write_obo(obo_path)
    convert_to_obograph(input_path=obo_path, json_path=stub.with_suffix(".json"))
    convert(input_path=obo_path, output_path=stub.with_suffix(".owl"))
    make_site(ontology, DOCS, manifest=True)


if __name__ == "__main__":
    _main()
