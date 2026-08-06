"""End-to-end compilation pipeline.

``compile_source`` runs the full pipeline: lexing, parsing, semantic
validation, default resolution and HTML generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from antlr4 import CommonTokenStream, InputStream

from compiler.ast import Document
from compiler.build_ast import build_ast
from compiler.codegen.html import render_html
from compiler.errors import LinkoraError, ParseError, SourcePosition
from compiler.generated.LinkoraLexer import LinkoraLexer
from compiler.generated.LinkoraParser import LinkoraParser
from compiler.validator import Validator


@dataclass
class CompilationResult:
    """The outcome of compiling one source document."""

    errors: list[LinkoraError]
    html: Optional[str] = None
    ast: Optional[Document] = None

    @property
    def success(self) -> bool:
        return not self.errors


class _ErrorListener:
    """Collects ANTLR syntax errors as :class:`ParseError` instances."""

    def __init__(self) -> None:
        self.errors: list[ParseError] = []

    def syntaxError(
        self,
        recognizer,
        offending_symbol,
        line: int,
        column: int,
        message: str,
        exception,
    ) -> None:
        self.errors.append(
            ParseError(
                f"Syntax error: {message}",
                SourcePosition(line=line, column=column + 1),
            )
        )


def _parse(source: str) -> tuple[Optional[object], list[ParseError]]:
    lexer = LinkoraLexer(InputStream(source))
    lexer_errors = _ErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexer_errors)

    tokens = CommonTokenStream(lexer)
    parser = LinkoraParser(tokens)
    parser_errors = _ErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(parser_errors)

    tree = parser.document()
    errors = lexer_errors.errors + parser_errors.errors
    return (None if errors else tree), errors


def compile_source(source: str) -> CompilationResult:
    """Compile a Linkora source string into a static HTML page."""
    tree, parse_errors = _parse(source)
    if parse_errors:
        return CompilationResult(errors=parse_errors)

    assert tree is not None
    document = build_ast(tree)

    validator = Validator()
    semantic_errors = validator.validate(document)
    if semantic_errors:
        return CompilationResult(errors=semantic_errors, ast=document)

    validator.resolve(document)
    return CompilationResult(errors=[], html=render_html(document), ast=document)
