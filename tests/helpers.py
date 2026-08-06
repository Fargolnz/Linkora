"""Helpers shared by the test modules."""

from __future__ import annotations

from compiler import CompilationResult, ParseError, SemanticError, compile_source


def compile_ok(source: str) -> CompilationResult:
    result = compile_source(source)
    assert result.success, "\n".join(error.format() for error in result.errors)
    return result


def compile_fails(source: str, error_type=SemanticError) -> list:
    result = compile_source(source)
    assert not result.success, "expected compilation to fail"
    assert result.errors, "expected at least one error"
    assert isinstance(result.errors[0], error_type), (
        f"expected {error_type.__name__}, got {type(result.errors[0]).__name__}: "
        f"{result.errors[0].format()}"
    )
    return result.errors


def compile_parse_fails(source: str) -> list:
    return compile_fails(source, error_type=ParseError)
