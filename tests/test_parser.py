"""Tests for lexical and syntactic analysis."""

from __future__ import annotations

import pytest

from tests.helpers import compile_fails, compile_ok, compile_parse_fails


class TestValidSyntax:
    def test_minimal_page(self):
        compile_ok("Page {\n}\n")

    def test_empty_page(self):
        compile_ok("Page {}")

    def test_single_link_expanded(self):
        compile_ok(
            'Page {\n'
            '    Link {\n'
            '        title: "GitHub"\n'
            '        url: "https://github.com"\n'
            '    }\n'
            '}\n'
        )

    def test_single_line_compact(self):
        compile_ok('Page { Link { title: "GitHub", url: "https://github.com" } }')

    def test_compact_with_trailing_comma(self):
        compile_ok('Page { Link { title: "GitHub", url: "https://github.com", } }')

    def test_compact_multiline(self):
        compile_ok(
            'Page {\n'
            '    Link {\n'
            '        title: "GitHub",\n'
            '        url: "https://github.com"\n'
            '    }\n'
            '}\n'
        )

    def test_multiple_links(self):
        compile_ok(
            'Page {\n'
            '    Link { title: "A", url: "https://a.com" }\n'
            '    Link { title: "B", url: "https://b.com" }\n'
            '}\n'
        )

    def test_comments(self):
        compile_ok(
            '// top-level comment\n'
            'Page {\n'
            '    // before a link\n'
            '    Link { title: "GitHub", url: "https://github.com" } // after\n'
            '}\n'
        )

    def test_whitespace_insensitive(self):
        source = 'Page{Link{title:"GitHub" url:"https://github.com"}}'
        compile_ok(source)

    def test_string_escape_sequences(self):
        compile_ok(
            'Page {\n'
            '    Link {\n'
            '        title: "He said \\"Hello\\"\\nLine 2"\n'
            '        url: "https://github.com"\n'
            '    }\n'
            '}\n'
        )


class TestInvalidSyntax:
    def test_link_outside_page(self):
        compile_parse_fails('Link { title: "GitHub", url: "https://github.com" }\n')

    def test_two_pages(self):
        compile_parse_fails('Page {}\nPage {}\n')

    def test_missing_closing_brace(self):
        compile_parse_fails('Page {\n    Link { title: "GitHub" \n')

    def test_unquoted_string_value(self):
        compile_parse_fails('Page { Link { title: GitHub, url: "https://x.com" } }')

    def test_single_quoted_string(self):
        compile_parse_fails('Page { Link { title: \'GitHub\', url: "https://x.com" } }')

    def test_unsupported_escape_sequence(self):
        compile_parse_fails(
            'Page { Link { title: "bad\\xescape", url: "https://x.com" } }'
        )

    def test_uppercase_property_name(self):
        compile_parse_fails('Page { Link { Title: "x", url: "https://x.com" } }')

    def test_number_value_is_valid_syntax(self):
        # A Number is a valid value syntactically; type checking is semantic.
        compile_fails('Page { Link { title: "x", url: 123 } }')

    def test_missing_colon(self):
        compile_parse_fails('Page { Link { title "x", url: "https://x.com" } }')
