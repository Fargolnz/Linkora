"""Compiler error types and source locations.

All compiler diagnostics are represented as ``LinkoraError`` subclasses and
formatted in a consistent, human-readable way.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SourcePosition:
    """A 1-based position inside a source file."""

    line: int
    column: int


class LinkoraError(Exception):
    """Base class for all Linkora compiler errors."""

    kind = "Compiler Error"

    def __init__(self, message: str, position: Optional[SourcePosition] = None):
        super().__init__(message)
        self.message = message
        self.position = position

    def format(self) -> str:
        if self.position is not None:
            return (
                f"{self.kind}\n"
                f"{self.message}\n"
                f"Line {self.position.line}, Column {self.position.column}."
            )
        return f"{self.kind}\n{self.message}"


class ParseError(LinkoraError):
    """Raised when the source text cannot be tokenized or parsed."""

    kind = "Parse Error"


class SemanticError(LinkoraError):
    """Raised when a parsed document violates a semantic rule."""

    kind = "Semantic Error"
