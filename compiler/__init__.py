"""Linkora compiler.

The package exposes the compilation pipeline and its public error types so
that both the CLI and external tooling can use them.
"""

from compiler.errors import LinkoraError, ParseError, SemanticError
from compiler.pipeline import CompilationResult, compile_source

__all__ = [
    "CompilationResult",
    "LinkoraError",
    "ParseError",
    "SemanticError",
    "compile_source",
]
