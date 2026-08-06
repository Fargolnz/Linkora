"""Tests for HTML code generation."""

from __future__ import annotations

from tests.helpers import compile_ok

PAGE = (
    "Page {\n"
    '    Link { title: "GitHub", url: "https://github.com" }\n'
    "}\n"
)


def _html(source: str = PAGE) -> str:
    result = compile_ok(source)
    assert result.html is not None
    return result.html


class TestPageShell:
    def test_doctype_and_lang(self):
        html = _html()
        assert html.startswith("<!DOCTYPE html>")
        assert '<html lang="en">' in html

    def test_page_container(self):
        html = _html()
        assert '<main class="lk-page">' in html
        assert "</main>" in html

    def test_styles_embedded(self):
        html = _html()
        assert "<style>" in html
        assert ".lk-link" in html
        assert ".lk-shape-rounded" in html
        assert ".lk-align-center" in html


class TestResponsiveDesign:
    def test_theme_background_variable(self):
        html = _html()
        assert "--lk-bg: #e0f4f4" in html
        assert "background-color: var(--lk-bg)" in html

    def test_mobile_first_page(self):
        html = _html()
        assert "min-height: 100dvh" in html
        assert "min-height: 100vh" in html

    def test_desktop_media_query(self):
        html = _html()
        assert "@media (min-width: 600px)" in html
        assert "max-width: 560px" in html

    def test_floating_card_styles(self):
        html = _html()
        assert "border-radius: 20px" in html
        assert "box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08)" in html

    def test_link_touch_target(self):
        html = _html()
        assert "min-height: 52px" in html


class TestLinkRendering:
    def test_renders_anchor(self):
        html = _html()
        assert (
            '<a class="lk-link lk-shape-rounded lk-align-center" '
            'style="color: #FFFFFF; background-color: #00B4B0; '
            'border-color: transparent;" href="https://github.com">GitHub</a>'
        ) in html

    def test_custom_visual_properties(self):
        html = _html(
            "Page {\n"
            '    Link { title: "Portfolio", url: "https://example.com", '
            'align: left, shape: pill, backgroundColor: "#3B82F6", '
            'titleColor: "#000000", borderColor: "#2563EB" }\n'
            "}\n"
        )
        assert 'class="lk-link lk-shape-pill lk-align-left"' in html
        assert (
            'style="color: #000000; background-color: #3B82F6; '
            'border-color: #2563EB;"'
        ) in html

    def test_multiple_links_rendered_in_order(self):
        html = _html(
            "Page {\n"
            '    Link { title: "First", url: "https://a.com" }\n'
            '    Link { title: "Second", url: "https://b.com" }\n'
            "}\n"
        )
        first = html.index(">First</a>")
        second = html.index(">Second</a>")
        assert first < second

    def test_html_escaping(self):
        html = _html(
            "Page {\n"
            '    Link { title: "He said \\"Hi & Bye\\"", '
            'url: "https://x.com/?a=1&b=2" }\n'
            "}\n"
        )
        assert "He said &quot;Hi &amp; Bye&quot;" in html
        assert 'href="https://x.com/?a=1&amp;b=2"' in html

    def test_newline_escape_rendered_as_newline(self):
        html = _html(
            "Page {\n"
            '    Link { title: "Line1\\nLine2", url: "https://x.com" }\n'
            "}\n"
        )
        assert "Line1\nLine2" in html
