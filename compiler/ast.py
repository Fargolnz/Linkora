"""Intermediate representation (AST) for Linkora documents.

The AST is produced by :mod:`compiler.build_ast` from the ANTLR parse tree and
consumed by the semantic validator and the code generators.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from compiler.errors import SourcePosition

# Raw value kinds produced by the lexer. Each kind maps to a decoded Python
# value (see ``Property.value``).
KIND_STRING = "STRING"
KIND_NUMBER = "NUMBER"
KIND_BOOLEAN = "BOOLEAN"
KIND_IDENTIFIER = "IDENTIFIER"

#: Escape sequences supported inside string literals.
_ESCAPES = {
    "t": "\t",
    "n": "\n",
    "r": "\r",
    '"': '"',
    "\\": "\\",
}


def unescape_string(inner: str) -> str:
    """Resolve the supported escape sequences in ``inner``.

    ``inner`` is the string literal body without the surrounding quotes.
    """
    out: list[str] = []
    i = 0
    while i < len(inner):
        char = inner[i]
        if char == "\\" and i + 1 < len(inner):
            out.append(_ESCAPES[inner[i + 1]])
            i += 2
        else:
            out.append(char)
            i += 1
    return "".join(out)


@dataclass
class Property:
    """A single ``name: value`` pair inside a block."""

    name: str
    #: Raw token text as written in the source (string literals include quotes).
    text: str
    #: One of the ``KIND_*`` constants.
    kind: str
    #: Decoded Python value (``str``, ``int``, ``float`` or ``bool``).
    value: object
    position: SourcePosition


@dataclass
class Block:
    """A named block with properties and optional child blocks."""

    name: str
    position: SourcePosition
    properties: list[Property] = field(default_factory=list)
    children: list["Block"] = field(default_factory=list)
    #: Filled by the validator with every property resolved to its final value.
    resolved: dict[str, object] = field(default_factory=dict)

    def property(self, name: str) -> Optional[Property]:
        for prop in self.properties:
            if prop.name == name:
                return prop
        return None


@dataclass
class Document:
    """A fully parsed Linkora document (one ``Page`` block)."""

    page: Block
