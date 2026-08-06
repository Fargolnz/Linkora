"""Tests for semantic validation and default resolution."""

from __future__ import annotations

from tests.helpers import compile_ok

LINK = 'Link { title: "GitHub", url: "https://github.com" }'


def _page(body: str) -> str:
    return f"Page {{\n    {body}\n}}\n"


class TestRequiredProperties:
    def test_missing_url(self):
        from compiler import SemanticError, compile_source

        errors = compile_source(_page('Link { title: "GitHub" }')).errors
        assert len(errors) == 1
        assert isinstance(errors[0], SemanticError)
        assert "required property 'url'" in errors[0].message

    def test_missing_title_reports_title(self):
        from compiler import compile_source

        errors = compile_source(_page('Link { url: "https://github.com" }')).errors
        assert len(errors) == 1
        assert "required property 'title'" in errors[0].message


class TestPropertyRules:
    def test_unknown_property(self):
        from compiler import compile_source

        errors = compile_source(
            _page('Link { title: "x", url: "https://x.com", fontSize: 18 }')
        ).errors
        assert len(errors) == 1
        assert "Unknown property 'fontSize'" in errors[0].message

    def test_duplicate_property(self):
        from compiler import compile_source

        errors = compile_source(
            _page('Link { title: "a", title: "b", url: "https://x.com" }')
        ).errors
        assert len(errors) == 1
        assert "Duplicate property 'title'" in errors[0].message


class TestValueValidation:
    def test_invalid_enum_value(self):
        from compiler import compile_source

        errors = compile_source(
            _page('Link { title: "x", url: "https://x.com", shape: roundedLarge }')
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message
        assert "sharp, slightlyRounded, rounded, pill" in errors[0].message

    def test_quoted_enum_value(self):
        from compiler import compile_source

        errors = compile_source(
            _page('Link { title: "x", url: "https://x.com", align: "center" }')
        ).errors
        assert len(errors) == 1
        assert "quotation marks" in errors[0].message

    def test_invalid_url_missing_scheme(self):
        from compiler import compile_source

        errors = compile_source(_page('Link { title: "x", url: "github.com" }')).errors
        assert len(errors) == 1
        assert "URL" in errors[0].message

    def test_invalid_url_unsupported_scheme(self):
        from compiler import compile_source

        errors = compile_source(
            _page('Link { title: "x", url: "ftp://github.com" }')
        ).errors
        assert len(errors) == 1
        assert "URL" in errors[0].message

    def test_invalid_color(self):
        from compiler import compile_source

        errors = compile_source(
            _page('Link { title: "x", url: "https://x.com", backgroundColor: "red" }')
        ).errors
        assert len(errors) == 1
        assert "Color" in errors[0].message

    def test_invalid_type_boolean_for_string(self):
        from compiler import compile_source

        errors = compile_source(
            _page('Link { title: true, url: "https://x.com" }')
        ).errors
        assert len(errors) == 1
        assert "String" in errors[0].message

    def test_valid_transparent_border(self):
        compile_ok(_page('Link { title: "x", url: "https://x.com", borderColor: transparent }'))

    def test_valid_hex_color_short(self):
        compile_ok(_page('Link { title: "x", url: "https://x.com", titleColor: "#FFF" }'))

    def test_all_optional_properties(self):
        compile_ok(
            _page(
                'Link {\n'
                '        title: "Portfolio"\n'
                '        url: "https://example.com"\n'
                '        align: left\n'
                '        titleColor: "#FFFFFF"\n'
                '        backgroundColor: "#3B82F6"\n'
                '        borderColor: "#2563EB"\n'
                '        shape: pill\n'
                '    }'
            )
        )


class TestBlockRules:
    def test_unknown_block(self):
        from compiler import SemanticError, compile_source

        errors = compile_source(_page('MagicButton {}')).errors
        assert len(errors) == 1
        assert isinstance(errors[0], SemanticError)
        assert "Unknown block 'MagicButton'" in errors[0].message

    def test_nested_page_rejected(self):
        from compiler import compile_source

        errors = compile_source(_page('Page {}')).errors
        assert len(errors) == 1
        assert "may appear only once" in errors[0].message or "Parse" in errors[0].kind

    def test_repeatable_links_allowed(self):
        compile_ok(_page(f"{LINK}\n    {LINK}"))


class TestDefaultResolution:
    def _first_link(self, source: str):
        result = compile_ok(source)
        assert result.ast is not None
        return result.ast.page.children[0]

    def test_defaults_applied(self):
        block = self._first_link(_page(LINK))
        assert block.resolved == {
            "title": "GitHub",
            "url": "https://github.com",
            "align": "center",
            "titleColor": "#FFFFFF",
            "backgroundColor": "#00B4B0",
            "borderColor": "transparent",
            "shape": "rounded",
        }

    def test_explicit_values_override_defaults(self):
        block = self._first_link(
            _page(
                'Link { title: "x", url: "https://x.com", '
                'align: right, shape: pill, backgroundColor: "#000000" }'
            )
        )
        assert block.resolved["align"] == "right"
        assert block.resolved["shape"] == "pill"
        assert block.resolved["backgroundColor"] == "#000000"
        assert block.resolved["titleColor"] == "#FFFFFF"

    def test_escape_sequences_decoded(self):
        block = self._first_link(
            _page('Link { title: "He said \\"Hi\\"\\nNext", url: "https://x.com" }')
        )
        assert block.resolved["title"] == 'He said "Hi"\nNext'
