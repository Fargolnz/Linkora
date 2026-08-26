"""HTML generation for validated Linkora documents.

Every block type has a ``render_<block>`` function. The dispatch table at the
bottom of this module maps block names to their renderer, so adding a new
block requires registering a single new renderer.
"""

from __future__ import annotations

import html

from compiler.ast import Block, Document
from compiler.codegen.css import build_css


def render_html(document: Document) -> str:
    """Render a validated document into a complete HTML page."""
    body = "\n".join(_render_block(block) for block in document.blocks)

    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\">\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
        "  <link href=\"https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700&display=swap\" rel=\"stylesheet\">\n"
        "  <title>Linkora</title>\n"
        "  <style>\n"
        f"{build_css()}"
        "  </style>\n"
        "</head>\n"
        "<body>\n"
        f"  <main class=\"lk-page\">\n{body}\n  </main>\n"
        "</body>\n"
        "</html>\n"
    )


def _render_block(block: Block) -> str:
    renderer = _RENDERERS.get(block.name)
    if renderer is None:
        return f"<!-- unsupported block: {html.escape(block.name)} -->"
    return renderer(block)


def render_link(block: Block) -> str:
    """Render a Link block as a clickable, styled button."""
    resolved = block.resolved
    title = str(resolved["title"])
    url = str(resolved["url"])
    shape = str(resolved["shape"])
    align = str(resolved["align"])
    title_color = str(resolved["titleColor"])
    background_color = str(resolved["backgroundColor"])
    border_color = str(resolved["borderColor"])

    classes = " ".join(["lk-link", f"lk-shape-{shape}", f"lk-align-{align}"])
    style = (
        f"color: {title_color}; "
        f"background-color: {background_color}; "
        f"border-color: {border_color};"
    )

    return (
        f'    <a class="{classes}" style="{style}" '
        f'href="{html.escape(url, quote=True)}">'
        f"{html.escape(title)}</a>"
    )


#: Dispatch table mapping block names to their HTML renderers.
_RENDERERS = {
    "Link": render_link,
}
