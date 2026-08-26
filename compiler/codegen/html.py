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


_PROFILE_CHILD_ORDER = ["Cover", "Logo", "Name", "Bio"]


def render_profile(block: Block) -> str:
    """Render a Profile container, sorting children into display order."""
    sorted_children = sorted(
        block.children,
        key=lambda c: _PROFILE_CHILD_ORDER.index(c.name)
        if c.name in _PROFILE_CHILD_ORDER
        else len(_PROFILE_CHILD_ORDER),
    )
    inner = "\n".join(_render_block(child) for child in sorted_children)
    return f'  <section class="lk-profile">\n{inner}\n  </section>'


def render_name(block: Block) -> str:
    """Render a Name block with title and subtitle."""
    resolved = block.resolved
    title = str(resolved["title"])
    subtitle = str(resolved["subtitle"])
    text_align = str(resolved["textAlign"])
    title_color = str(resolved["titleColor"])
    sub_color = str(resolved["subColor"])

    parts = []
    if title:
        parts.append(
            f'    <h1 class="lk-name-title" '
            f'style="color: {title_color};">{html.escape(title)}</h1>'
        )
    if subtitle:
        parts.append(
            f'    <p class="lk-name-subtitle" '
            f'style="color: {sub_color};">{html.escape(subtitle)}</p>'
        )

    inner = "\n".join(parts)
    return (
        f'  <div class="lk-name lk-align-{text_align}">\n'
        f"{inner}\n"
        f"  </div>"
    )


def render_logo(block: Block) -> str:
    """Render a Logo block as a profile image."""
    resolved = block.resolved
    image = str(resolved["image"])
    shape = str(resolved["shape"])
    border_color = str(resolved["borderColor"])

    style = f"border-color: {border_color};"
    return (
        f'    <img class="lk-logo lk-logo-{shape}" '
        f'style="{style}" '
        f'src="{html.escape(image, quote=True)}" alt="Logo">'
    )


def render_bio(block: Block) -> str:
    """Render a Bio block as a styled paragraph."""
    resolved = block.resolved
    bio = str(resolved["bio"])
    text_align = str(resolved["textAlign"])
    text_color = str(resolved["textColor"])
    bg_color = str(resolved["backgroundColor"])
    border_color = str(resolved["borderColor"])
    shape = str(resolved["shape"])

    classes = " ".join(["lk-bio", f"lk-shape-{shape}"])
    style = (
        f"color: {text_color}; "
        f"background-color: {bg_color}; "
        f"border-color: {border_color}; "
        f"text-align: {text_align};"
    )
    return (
        f'    <p class="{classes}" style="{style}">'
        f"{html.escape(bio)}</p>"
    )


def render_cover(block: Block) -> str:
    """Render a Cover block as a full-width banner image."""
    resolved = block.resolved
    image = str(resolved["image"])
    shape = str(resolved["shape"])

    classes = " ".join(["lk-cover", f"lk-cover-{shape}"])
    return (
        f'  <div class="{classes}">\n'
        f'    <img class="lk-cover-img" '
        f'src="{html.escape(image, quote=True)}" alt="Cover">\n'
        f"  </div>"
    )


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
    "Profile": render_profile,
    "Name": render_name,
    "Logo": render_logo,
    "Bio": render_bio,
    "Cover": render_cover,
    "Link": render_link,
}
