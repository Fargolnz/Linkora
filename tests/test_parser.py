"""Tests for lexical and syntactic analysis."""

from __future__ import annotations

import pytest

from tests.helpers import compile_fails, compile_ok, compile_parse_fails


class TestValidSyntax:
    def test_minimal_document(self):
        compile_ok("")

    def test_empty_document(self):
        compile_ok("   \n\n")

    def test_single_link_expanded(self):
        compile_ok(
            'Link {\n'
            '    title: "GitHub"\n'
            '    url: "https://github.com"\n'
            '}\n'
        )

    def test_single_line_compact(self):
        compile_ok('Link { title: "GitHub", url: "https://github.com" }')

    def test_compact_with_trailing_comma(self):
        compile_ok('Link { title: "GitHub", url: "https://github.com", }')

    def test_compact_multiline(self):
        compile_ok(
            'Link {\n'
            '    title: "GitHub",\n'
            '    url: "https://github.com"\n'
            '}\n'
        )

    def test_multiple_links(self):
        compile_ok(
            'Link { title: "A", url: "https://a.com" }\n'
            'Link { title: "B", url: "https://b.com" }\n'
        )

    def test_single_title(self):
        compile_ok('Title { title: "My Links" }')

    def test_title_compact_multiline(self):
        compile_ok(
            'Title {\n'
            '    title: "My Links"\n'
            '    align: left\n'
            '    titleColor: "#c7006e"\n'
            '}\n'
        )

    def test_comments(self):
        compile_ok(
            '// top-level comment\n'
            '// before a link\n'
            'Link { title: "GitHub", url: "https://github.com" } // after\n'
        )

    def test_whitespace_insensitive(self):
        compile_ok('Link{title:"GitHub" url:"https://github.com"}')

    def test_string_escape_sequences(self):
        compile_ok(
            'Link {\n'
            '    title: "He said \\"Hello\\"\\nLine 2"\n'
            '    url: "https://github.com"\n'
            '}\n'
        )

    def test_profile_with_children(self):
        compile_ok(
            'Profile {\n'
            '    Name { title: "Test" }\n'
            '    Logo { image: "https://example.com/photo.jpg" }\n'
            '    Bio { bio: "Hello" }\n'
            '    Cover { image: "https://example.com/cover.jpg" }\n'
            '}\n'
        )

    def test_profile_empty(self):
        compile_ok('Profile {}')

    def test_profile_partial_children(self):
        compile_ok(
            'Profile {\n'
            '    Name { title: "Test" }\n'
            '}\n'
        )

    def test_profile_and_links(self):
        compile_ok(
            'Profile {\n'
            '    Name { title: "Test" }\n'
            '}\n'
            'Link { title: "GitHub", url: "https://github.com" }\n'
        )


class TestInvalidSyntax:
    def test_missing_closing_brace(self):
        compile_parse_fails('Link { title: "GitHub" \n')

    def test_unquoted_string_value(self):
        compile_parse_fails('Link { title: GitHub, url: "https://x.com" }')

    def test_single_quoted_string(self):
        compile_parse_fails('Link { title: \'GitHub\', url: "https://x.com" }')

    def test_unsupported_escape_sequence(self):
        compile_parse_fails(
            'Link { title: "bad\\xescape", url: "https://x.com" }'
        )

    def test_uppercase_property_name(self):
        compile_parse_fails('Link { Title: "x", url: "https://x.com" }')

    def test_number_value_is_valid_syntax(self):
        # A Number is a valid value syntactically; type checking is semantic.
        compile_fails('Link { title: "x", url: 123 }')

    def test_missing_colon(self):
        compile_parse_fails('Link { title "x", url: "https://x.com" }')
