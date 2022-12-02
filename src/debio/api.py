# -*- coding: utf-8 -*-

"""Main code."""

import logging
from pathlib import Path
from typing import Iterable, List, Optional

from pyobo import Obo, Reference, SynonymTypeDef, Term, TypeDef

from debio.resources import PROPERTIES, TERMS, TYPEDEFS
from debio.version import VERSION

__all__ = [
    "DecentralizedBiomedicalOntology",
]

logger = logging.getLogger(__name__)

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.parent.resolve()
DOCS = ROOT.joinpath("docs")

PREFIX = "debio"
URI_PREFIX = "https://biopragmatics.github.io/debio/"
IDSPACES = {
    PREFIX: URI_PREFIX,
    "RO": "http://purl.obolibrary.org/obo/RO_",
    "obo": "http://purl.obolibrary.org/obo/",
    "orcid": "https://orcid.org/",
}


def get_typedefs() -> Iterable[TypeDef]:
    """Get type definitions and properties."""
    for typedef in TYPEDEFS:
        yield _get_typedef(typedef)
    for prop in PROPERTIES:
        yield _get_typedef(prop, is_metadata_tag=True)


def _reference_list(references) -> List[Reference]:
    return [
        Reference(
            prefix=reference["prefix"],
            identifier=reference["identifier"],
            name=reference.get("name"),
        )
        for reference in references
    ]


def _get_typedef(typedef, is_metadata_tag: Optional[bool] = None) -> TypeDef:
    return TypeDef(
        reference=Reference(
            prefix=PREFIX,
            identifier=typedef["identifier"],
            name=typedef["name"],
        ),
        definition=typedef.get("description"),
        holds_over_chain=_reference_list(typedef.get("holds_over_chain", [])),
        is_metadata_tag=is_metadata_tag,
        xrefs=_reference_list(typedef.get("xrefs", [])),
        created_by=f"orcid:{typedef['creator']}",
        parents=_reference_list(typedef.get("parents", [])),
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
    data_version = VERSION

    def iter_terms(self, force: bool = False) -> Iterable[Term]:
        """Iterate over terms in the ontology."""
        return get_terms()

    def _get_version(self) -> str:
        return VERSION


def write(ontology: Obo, directory: Path) -> None:
    """Write ontology artifacts."""
    from bioontologies.robot import convert, convert_to_obograph, is_available

    directory.mkdir(exist_ok=True, parents=True)
    stub = directory.joinpath(ontology.ontology)
    obo_path = stub.with_suffix(".obo")
    ontology.write_obo(obo_path)
    if not is_available():
        logger.warning("ROBOT is not available - can not create OWL and OBO Graph JSON artifacts")
    else:
        convert_to_obograph(input_path=obo_path, json_path=stub.with_suffix(".json"))
        convert(
            input_path=obo_path,
            output_path=stub.with_suffix(".owl"),
            extra_args=[
                "--prefix",
                f"'{PREFIX}: {URI_PREFIX}'",
            ],
        )
