"""Declarative definition of the Linkora language.

Every block and every property accepted by the language is described here as
plain data. Adding a new block to the language is a matter of:

1. Adding a ``PropertyDef`` tuple for its properties, and
2. Registering a ``BlockDef`` in the :data:`BLOCKS` table.
3. Adding a renderer for it in :mod:`compiler.codegen`.

Semantic validation and code generation are driven entirely by this data, so
no other compiler code needs to change.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ValueType(Enum):
    """The set of property value types supported by the language."""

    STRING = "String"
    NUMBER = "Number"
    BOOLEAN = "Boolean"
    COLOR = "Color"
    URL = "URL"
    FILE = "File"
    ENUM = "Enum"


@dataclass(frozen=True)
class PropertyDef:
    """The definition of a single block property."""

    name: str
    type: ValueType
    default: object
    required: bool = False
    enum_values: tuple[str, ...] = ()


@dataclass(frozen=True)
class BlockDef:
    """The definition of a single block."""

    name: str
    #: Name of the only parent block that may contain this block, or ``None``
    #: for the root ``Page`` block.
    parent: Optional[str]
    repeatable: bool = False
    allowed_children: tuple[str, ...] = ()
    properties: dict[str, "PropertyDef"] = field(default_factory=dict)

    def property(self, name: str) -> Optional[PropertyDef]:
        return self.properties.get(name)


def _properties(*defs: PropertyDef) -> dict[str, PropertyDef]:
    return {prop.name: prop for prop in defs}


# ---------------------------------------------------------------------------
# Block definitions
# ---------------------------------------------------------------------------

_LINK = BlockDef(
    name="Link",
    parent=None,
    repeatable=True,
    properties=_properties(
        PropertyDef("title", ValueType.STRING, "", required=True),
        PropertyDef("url", ValueType.URL, "", required=True),
        PropertyDef(
            "align",
            ValueType.ENUM,
            "center",
            enum_values=("left", "center", "right"),
        ),
        PropertyDef("titleColor", ValueType.COLOR, "#FFFFFF"),
        PropertyDef("backgroundColor", ValueType.COLOR, "#00B4B0"),
        PropertyDef("borderColor", ValueType.COLOR, "transparent"),
        PropertyDef(
            "shape",
            ValueType.ENUM,
            "rounded",
            enum_values=("sharp", "slightlyRounded", "rounded", "pill"),
        ),
    ),
)

#: The full set of blocks known to the compiler, keyed by block name.
BLOCKS: dict[str, BlockDef] = {
    _LINK.name: _LINK,
}


def get_block(name: str) -> Optional[BlockDef]:
    return BLOCKS.get(name)
