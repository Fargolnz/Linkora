"""End-to-end compilation pipeline.

``compile_source`` runs the full pipeline: lexing, parsing, semantic
validation, default resolution and HTML generation.

``compile_file`` extends this with local image file copying for CLI usage.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from antlr4 import CommonTokenStream, InputStream

from compiler.ast import Block, Document
from compiler.build_ast import build_ast
from compiler.codegen.html import render_html
from compiler.errors import LinkoraError, ParseError, SourcePosition
from compiler.generated.LinkoraLexer import LinkoraLexer
from compiler.generated.LinkoraParser import LinkoraParser
from compiler.schema import BLOCKS, ValueType
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


# ---------------------------------------------------------------------------
# Local image file handling
# ---------------------------------------------------------------------------

def _is_local_path(value: str) -> bool:
    """True if the value is a local file path (not a URL)."""
    return not value.startswith(("http://", "https://"))


def collect_image_paths(document: Document) -> list[tuple[Block, str, str]]:
    """Return ``(block, property_name, local_path)`` for every IMAGE property
    that references a local file."""
    results: list[tuple[Block, str, str]] = []
    _walk_blocks(document.blocks, results)
    return results


def _walk_blocks(
    blocks: list[Block],
    results: list[tuple[Block, str, str]],
) -> None:
    for block in blocks:
        block_def = BLOCKS.get(block.name)
        if block_def is not None:
            for prop_name, prop_def in block_def.properties.items():
                if prop_def.type is ValueType.IMAGE:
                    value = block.resolved.get(prop_name, "")
                    if isinstance(value, str) and value and _is_local_path(value):
                        results.append((block, prop_name, value))
        _walk_blocks(block.children, results)


def copy_local_images(
    source_dir: Path,
    document: Document,
    output_dir: Path,
) -> None:
    """Copy every local IMAGE file into ``output_dir/assets/`` and rewrite
    the resolved values to the new relative paths."""
    assets_dir = output_dir / "assets"
    for block, prop_name, local_path in collect_image_paths(document):
        src = source_dir / local_path
        if not src.is_file():
            continue
        dest = assets_dir / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        block.resolved[prop_name] = f"assets/{src.name}"


def compile_file(source_path: Path, output_dir: Path) -> CompilationResult:
    """Compile a ``.lkr`` source file, copying local images to *output_dir*."""
    source_text = source_path.read_text(encoding="utf-8")
    tree, parse_errors = _parse(source_text)
    if parse_errors:
        return CompilationResult(errors=parse_errors)

    assert tree is not None
    document = build_ast(tree)

    validator = Validator()
    semantic_errors = validator.validate(document)
    if semantic_errors:
        return CompilationResult(errors=semantic_errors, ast=document)

    validator.resolve(document)
    copy_local_images(source_path.parent, document, output_dir)
    return CompilationResult(errors=[], html=render_html(document), ast=document)
