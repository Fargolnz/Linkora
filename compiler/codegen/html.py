"""HTML generation for validated Linkora documents.

Every block type has a ``render_<block>`` function. The dispatch table at the
bottom of this module maps block names to their renderer, so adding a new
block requires registering a single new renderer.
"""

from __future__ import annotations

import html

from compiler.ast import Block, Document
from compiler.codegen.css import build_css


#: Per-platform metadata for the SocialMedia block: canonical display name,
#: a full-color brand SVG icon (inline path data), and a soft shade of the
#: brand color used as the default item background.
PLATFORM_META: dict[str, dict[str, str]] = {
    "instagram": {
        "name": "Instagram",
        "bg": "#F3E9F2",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="ig" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#F09433"/><stop offset="0.25" '
            'stop-color="#E6683C"/><stop offset="0.5" stop-color="#DC2743"/>'
            '<stop offset="0.75" stop-color="#CC2366"/><stop offset="1" '
            'stop-color="#BC1888"/></linearGradient></defs>'
            '<rect width="24" height="24" rx="5" fill="url(#ig)"/>'
            '<circle cx="12" cy="12" r="4" fill="none" stroke="#fff" '
            'stroke-width="1.6"/><circle cx="17.2" cy="6.8" r="1.1" fill="#fff"/>'
            "</svg>"
        ),
    },
    "telegram": {
        "name": "Telegram",
        "bg": "#E3F2FD",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#29B6F6" d="M21.6 4.3 2.9 10.9c-1.2.5-1.1 1.9.2 '
            '2.2l4.7 1.5 1.8 5.7c.3.9 1.4 1.2 2.1.5l2.5-2.4 4.9 3.6c.8.6 '
            '1.9.1 2.1-.9l3-14.1c.2-1.1-.9-2-1.9-1.7zM9.5 13.9l8-5.4c.3-.2.6.1.3.4'
            'l-6.4 6-2.2-2.1 7.3-4.7c.3-.2.6.2.3.4L9.5 14z"/>'
            "</svg>"
        ),
    },
    "youtube": {
        "name": "YouTube",
        "bg": "#FDE9E9",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#FF0000" d="M23 7.2s-.2-1.6-.9-2.3c-.9-.9-1.8-.9-2.3-1'
            '-3.2-.2-8-.2-8-.2s-4.8 0-8 .2c-.5.1-1.4.1-2.3 1-.7.7-.9 2.3-.9 2.3S0 '
            '9.1 0 11v1.8c0 1.9.2 3.8.2 3.8s.2 1.6.9 2.3c.9.9 2 .9 2.6 1 1.9.2 '
            '8 .2 8 .2s4.8 0 8-.2c.5-.1 1.4-.1 2.3-1 .7-.7.9-2.3.9-2.3s.2-1.9 '
            '.2-3.8V11c-.1-1.9-.3-3.8-.3-3.8zM9.5 15.2V8.7l6.2 3.3-6.2 3.2z"/>'
            "</svg>"
        ),
    },
    "tiktok": {
        "name": "TikTok",
        "bg": "#E9F1F7",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#010101" d="M19.3 6.9a5.3 5.3 0 0 1-3.2-1.1 5.3 5.3 '
            '0 0 1-1.8-2.7h-3.2v12.4a3 3 0 1 1-2.1-2.9V9a6.2 6.2 0 1 0 5.3 '
            '6.1V8.8a8.6 8.6 0 0 0 5 1.6V7.3c-.1 0-.1 0-.1-.1z"/>'
            '<path fill="#25F4EE" d="M14.3 3.1h1.1c.2 1.3.8 2 1.6 2.7-1 .8-2.6 '
            '1.3-2.7 1.9V3.1z"/><path fill="#FE2C55" d="M19.3 6.9v2.6a8.6 8.6 0 0 '
            '1-5-1.6v6.1a6.2 6.2 0 1 1-5.3-6.1v3a3 3 0 1 0 2.1 2.9V3.1h3.2c.4 1.3 '
            '1.1 2.1 1.8 2.7.6.5 1.2.9 2 .1z"/>'
            "</svg>"
        ),
    },
    "x": {
        "name": "X",
        "bg": "#ECECEC",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#010101" d="M18.9 2H22l-6.8 7.8L23.3 22h-6.3l-4.9-6.5'
            '-5.7 6.5H1l7.3-8.4L1 2h6.5l4.4 6L18.9 2zm-1.1 18h1.7L7 3.9H5.1L17.8 '
            '20z"/>'
            "</svg>"
        ),
    },
    "linkedin": {
        "name": "LinkedIn",
        "bg": "#E7EEF7",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#0A66C2" d="M20.4 20.4h-3.6v-5.6c0-1.3 0-3-1.9-3-1.9 0'
            '-2.1 1.4-2.1 2.9v5.7H9.2V9h3.4v1.6h.1c.5-.9 1.6-1.9 3.4-1.9 3.6 0 '
            '4.3 2.4 4.3 5.5v6.2zM5.3 7.4a2.1 2.1 0 1 1 0-4.2 2.1 2.1 0 0 1 0 '
            '4.2zM7.1 20.4H3.5V9h3.6v11.4zM22.2 0H1.8C.8 0 0 .8 0 1.8v20.4c0 1 '
            '.8.8 1.8 1.8h20.4c1 0 1.8-.8 1.8-1.8V1.8c0-1-.8-1.8-1.8-1.8z"/>'
            "</svg>"
        ),
    },
    "github": {
        "name": "GitHub",
        "bg": "#E9ECEF",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#24292E" d="M12 0a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v'
            '-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.8.1-.8.1-.8 1.2 '
            '.1 1.9 1.2 1.9 1.2 1.1 1.9 2.9 1.3 3.6 1 .1-.8.4-1.3.8-1.6-2.7-.3'
            '-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.3-3.2-.1-.3-.6-1.5.1-3.2 0 0 1-.3 3.3 '
            '1.2a11.5 11.5 0 0 1 6 0C17.3 4.5 18.4 5 18.4 5c.7 1.7.2 2.9.1 3.2.8 '
            '.8 1.3 1.9 1.3 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2'
            '.7.8.6A12 12 0 0 0 12 0z"/>'
            "</svg>"
        ),
    },
    "spotify": {
        "name": "Spotify",
        "bg": "#E4F4E8",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#1DB954" d="M12 0a12 12 0 1 0 0 24 12 12 0 0 0 0-24zm5.5 '
            '17.3c-.2.3-.6.4-.9.2-2.5-1.5-5.6-1.9-9.3-1-.4.1-.7-.2-.8-.5-.1-.4.2-'
            '.7.5-.8 4-1 7.5-.5 10.3 1.2.3.1.4.5.2.9zm1.5-3.2c-.2.4-.7.5-1.1.3-'
            '2.9-1.8-7.2-2.3-10.6-1.3-.4.1-.9-.1-1-.5-.1-.4.1-.9.5-1 3.8-1.1 8.5-'
            '.5 11.8 1.5.4.2.5.7.4 1zm.1-3.4c-3.5-2.1-9.2-2.3-12.5-1.3-.5.2-1-.1-'
            '1.2-.6-.2-.5.1-1 .5-1.2 3.8-1.1 10.2-.9 14.2 1.5.4.3.6.8.4 1.2-.3.4-'
            '.8.6-1.4.4z"/>'
            "</svg>"
        ),
    },
    "twitch": {
        "name": "Twitch",
        "bg": "#EAE6F8",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#9146FF" d="M2 2h20v13.3l-4.7 4.7H12l-3.3 3h-2v-3H2V2zm2 '
            '2v11.3h3.3v2.2L9.6 15.3h3.6l3-3V4H4zm9.3 2h1.9v5.3h-1.9V6zm-4 0h1.9v'
            '5.3H9.3V6z"/>'
            "</svg>"
        ),
    },
    "pinterest": {
        "name": "Pinterest",
        "bg": "#F9E7E4",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#E60023" d="M12 0a12 12 0 0 0-4.4 23.2c-.1-.8-.2-2 .1-2.9'
            '.2-1 .7-2 .7-2s-.7-1.6-.7-2.9c0-2.7 1.6-4.7 3.5-4.7 1.7 0 2.5 1.3 2.5'
            ' 2.8 0 1.7-1.1 4.2-1.6 6.5-.5 1.9 1 3.4 2.9 3.4 3.4 0 6-3.6 6-8.9'
            ' 0-4.6-3.3-7.9-8-7.9-5.5 0-8.7 4.1-8.7 8.3 0 1.6.6 3.3 1.4 4.3.2.2.2'
            '.4.1.6l-.5 2c-.1.2-.3.3-.5.2-1.8-.9-3-3.6-3-5.9 0-4.8 3.5-9.2 10-9.2 '
            '5.3 0 8.9 3.8 8.9 8.9 0 5.3-3.3 9.5-8 9.5-1.6 0-3-.8-3.5-1.8l-1 '
            '3.7c-.3 1.2-1 2.6-1.6 3.6A12 12 0 1 0 12 0z"/>'
            "</svg>"
        ),
    },
    "facebook": {
        "name": "Facebook",
        "bg": "#E7EFFB",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#1877F2" d="M24 12a12 12 0 1 0-13.9 11.9v-8.4H7.1V12h3'
            'V9.4c0-3 1.8-4.7 4.5-4.7 1.3 0 2.6.2 2.6.2v2.9h-1.5c-1.5 0-1.9.9-1.9'
            ' 1.9V12h3.3l-.5 3.5h-2.8v8.4A12 12 0 0 0 24 12z"/>'
            "</svg>"
        ),
    },
    "patreon": {
        "name": "Patreon",
        "bg": "#FDE9E6",
        "icon": (
            '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
            '<path fill="#FF424D" d="M14.8 0a8 8 0 1 0 0 16.3 8 8 0 0 0 0-16.3zM4.4'
            ' 2.4v21.4h4.5V2.4H4.4z"/>'
            "</svg>"
        ),
    },
}


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
    align = str(resolved["align"])
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
        f'  <div class="lk-name lk-align-{align}">\n'
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
    text = str(resolved["text"])
    align = str(resolved["align"])
    text_color = str(resolved["textColor"])
    bg_color = str(resolved["backgroundColor"])
    border_color = str(resolved["borderColor"])
    shape = str(resolved["shape"])

    classes = " ".join(["lk-bio", f"lk-shape-{shape}"])
    style = (
        f"color: {text_color}; "
        f"background-color: {bg_color}; "
        f"border-color: {border_color}; "
        f"text-align: {align};"
    )
    return (
        f'    <p class="{classes}" style="{style}">'
        f"{html.escape(text)}</p>"
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


def render_title(block: Block) -> str:
    """Render a Title block as a styled heading."""
    resolved = block.resolved
    title = str(resolved["title"])
    align = str(resolved["align"])
    title_color = str(resolved["titleColor"])

    style = f"color: {title_color}; text-align: {align};"

    return (
        f'  <h2 class="lk-title" style="{style}">'
        f"{html.escape(title)}</h2>"
    )


def render_text(block: Block) -> str:
    """Render a Text block as a styled paragraph."""
    resolved = block.resolved
    text = str(resolved["text"])
    align = str(resolved["align"])
    text_color = str(resolved["textColor"])
    bg_color = str(resolved["backgroundColor"])
    border_color = str(resolved["borderColor"])
    shape = str(resolved["shape"])

    classes = " ".join(["lk-text", f"lk-shape-{shape}"])
    style = (
        f"color: {text_color}; "
        f"background-color: {bg_color}; "
        f"border-color: {border_color}; "
        f"text-align: {align};"
    )
    return (
        f'  <p class="{classes}" style="{style}">'
        f"{html.escape(text)}</p>"
    )


def render_socialmedia_item(block: Block) -> str:
    """Render a single SocialMedia item as a clickable styled button."""
    resolved = block.resolved
    parent = _parent_resolved(block)
    platform = str(resolved["platform"])
    meta = PLATFORM_META[platform]

    def inherit(key: str, parent_key: str, fallback: str = "") -> str:
        value = str(resolved[key])
        if value:
            return value
        pvalue = str(parent.get(parent_key, ""))
        if pvalue:
            return pvalue
        return fallback

    title = str(resolved["title"]) or meta["name"]
    url = str(resolved["url"])
    title_color = inherit("titleColor", "titleColor", "#1A1A1A")
    background_color = inherit("backgroundColor", "backgroundColor", meta["bg"])
    border_color = inherit("borderColor", "borderColor", "transparent")
    icon_color = str(resolved["iconColor"]) or str(parent.get("iconColor", "")) or ""

    show_title = bool(parent.get("showTitle", True))
    show_icon = bool(parent.get("showIcon", True))
    icon_position = str(parent.get("iconPosition", "right"))
    shape = str(parent.get("shape", "rounded"))

    classes = " ".join(
        ["lk-smitem", f"lk-shape-{shape}", f"lk-icon-{icon_position}"]
    )
    style = (
        f"color: {title_color}; "
        f"background-color: {background_color}; "
        f"border-color: {border_color};"
    )

    parts = []
    if show_icon:
        parts.append(_icon_svg(meta, icon_color))
    if show_title:
        parts.append(f'<span class="lk-smitem-title">{html.escape(title)}</span>')

    inner = "".join(parts)
    return (
        f'    <a class="{classes}" style="{style}" '
        f'href="{html.escape(url, quote=True)}">{inner}</a>'
    )


def render_socialmedia(block: Block) -> str:
    """Render a SocialMedia container as a responsive grid of items."""
    resolved = block.resolved
    columns = int(resolved["columns"])
    items_order = str(resolved["itemsOrder"])

    items = "\n".join(_render_block(child) for child in block.children)
    return (
        f'  <section class="lk-socialmedia" '
        f'data-columns="{columns}" data-order="{items_order}">\n'
        f"{items}\n"
        f"  </section>"
    )


def _parent_resolved(block: Block) -> dict[str, object]:
    """Return the resolved properties of the nearest ancestor block."""
    return block.parent.resolved if block.parent is not None else {}


def _icon_svg(meta: dict[str, str], icon_color: str) -> str:
    """Wrap a platform's inline SVG, optionally forcing a single icon color."""
    svg = meta["icon"]
    if icon_color:
        # Tint a monochrome-friendly icon by setting fill on path elements.
        import re

        svg = re.sub(r'fill="[^"]*"', f'fill="{html.escape(icon_color, quote=True)}"', svg)
        svg = re.sub(
            r'stroke="[^"]*"',
            f'stroke="{html.escape(icon_color, quote=True)}"',
            svg,
        )
    return f'<span class="lk-smitem-icon" aria-hidden="true">{svg}</span>'


#: Dispatch table mapping block names to their HTML renderers.
_RENDERERS = {
    "Profile": render_profile,
    "Name": render_name,
    "Logo": render_logo,
    "Bio": render_bio,
    "Cover": render_cover,
    "Link": render_link,
    "Title": render_title,
    "Text": render_text,
    "SocialMedia": render_socialmedia,
    "SocialMediaItem": render_socialmedia_item,
}
