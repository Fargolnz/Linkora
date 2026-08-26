"""Build the Linkora AST from the ANTLR parse tree."""

from __future__ import annotations

from antlr4 import ParseTreeWalker
from antlr4.Token import Token

from compiler.ast import (
    KIND_BOOLEAN,
    KIND_IDENTIFIER,
    KIND_NUMBER,
    KIND_STRING,
    Block,
    Document,
    Property,
    unescape_string,
)
from compiler.errors import SourcePosition
from compiler.generated.LinkoraListener import LinkoraListener
from compiler.generated.LinkoraParser import LinkoraParser


def _position(token: Token) -> SourcePosition:
    # ANTLR columns are zero-based; the public API is one-based.
    return SourcePosition(line=token.line, column=token.column + 1)


def _value_parts(value_ctx: LinkoraParser.ValueContext) -> tuple[str, str]:
    """Return ``(kind, raw_text)`` for a value rule context."""
    if value_ctx.STRING() is not None:
        return KIND_STRING, value_ctx.STRING().getText()
    if value_ctx.NUMBER() is not None:
        return KIND_NUMBER, value_ctx.NUMBER().getText()
    if value_ctx.booleanLiteral() is not None:
        return KIND_BOOLEAN, value_ctx.getText()
    return KIND_IDENTIFIER, value_ctx.IDENTIFIER().getText()


def _decode_value(kind: str, text: str) -> object:
    if kind == KIND_STRING:
        return unescape_string(text[1:-1])
    if kind == KIND_NUMBER:
        return float(text) if "." in text else int(text)
    if kind == KIND_BOOLEAN:
        return text == "true"
    return text


class _AstBuilder(LinkoraListener):
    def __init__(self) -> None:
        self.stack: list[Block] = []
        self.top_level: list[Block] = []

    def enterBlock(self, ctx: LinkoraParser.BlockContext) -> None:
        block = Block(
            name=ctx.BLOCK_NAME().getText(),
            position=_position(ctx.BLOCK_NAME().symbol),
        )
        if self.stack:
            self.stack[-1].children.append(block)
        else:
            self.top_level.append(block)
        self.stack.append(block)

    def exitBlock(self, ctx: LinkoraParser.BlockContext) -> None:
        self.stack.pop()

    def enterProperty(self, ctx: LinkoraParser.PropertyContext) -> None:
        name = ctx.IDENTIFIER().getText()
        kind, text = _value_parts(ctx.value())
        prop = Property(
            name=name,
            text=text,
            kind=kind,
            value=_decode_value(kind, text),
            position=_position(ctx.IDENTIFIER().symbol),
        )
        self.stack[-1].properties.append(prop)


def build_ast(tree: LinkoraParser.DocumentContext) -> Document:
    """Convert an ANTLR ``document`` parse tree into a :class:`Document`."""
    builder = _AstBuilder()
    ParseTreeWalker().walk(builder, tree)
    return Document(blocks=builder.top_level)
