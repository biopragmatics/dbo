"""Resources for DeBiO."""

import json
from pathlib import Path

__all__ = [
    "TERMS_PATH",
    "TERMS",
    "TYPEDEFS_PATH",
    "TYPEDEFS",
    "PROPERTIES_PATH",
    "PROPERTIES",
]

HERE = Path(__file__).parent.resolve()

TERMS_PATH = HERE.joinpath("terms.json")
TERMS = json.loads(TERMS_PATH.read_text())

TYPEDEFS_PATH = HERE.joinpath("typedefs.json")
TYPEDEFS = json.loads(TYPEDEFS_PATH.read_text())

PROPERTIES_PATH = HERE.joinpath("properties.json")
PROPERTIES = json.loads(PROPERTIES_PATH.read_text())
