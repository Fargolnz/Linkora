"""Shared CSS for generated Linkora pages.

Block-specific CSS classes are named ``lk-<block>-<variant>`` so that new
blocks can reuse the same conventions without collisions.
"""

from __future__ import annotations

#: Border-radius (px) for each ``shape`` value of the Link block.
LINK_SHAPES = {
    "sharp": "0",
    "slightlyRounded": "6px",
    "rounded": "12px",
    "pill": "999px",
}

#: CSS flex alignment for each ``align`` value of the Link block.
LINK_ALIGNMENTS = {
    "left": "flex-start",
    "center": "center",
    "right": "flex-end",
}

#: Light tint of the theme accent color (#00B4B0), used as the page
#: background. Overridable later through a Theme block via the --lk-bg
#: variable.
PAGE_BACKGROUND = "#e0f4f4"

#: Viewport width (px) above which the page becomes a floating card.
DESKTOP_BREAKPOINT = "600px"

_BASE_CSS = f"""
:root {{
    color-scheme: light;
    --lk-bg: {PAGE_BACKGROUND};
}}

* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
}}

body {{
    min-height: 100vh;
    min-height: 100dvh;
    background-color: var(--lk-bg);
    font-family: "Vazirmatn", -apple-system, BlinkMacSystemFont, "Segoe UI",
        Roboto, Helvetica, Arial, sans-serif;
}}

/* Mobile-first: the page fills the phone viewport. */
.lk-page {{
    max-width: 100%;
    min-height: 100vh;
    min-height: 100dvh;
    margin: 0 auto;
    padding: 24px 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.lk-link {{
    display: flex;
    align-items: center;
    width: 100%;
    min-height: 52px;
    padding: 16px 24px;
    border: 2px solid transparent;
    font-size: 16px;
    font-weight: 600;
    text-decoration: none;
    transition: transform 120ms ease, opacity 120ms ease;
}}

.lk-link:hover {{
    transform: translateY(-2px);
    opacity: 0.92;
}}

/* Larger screens: a column slightly wider than a phone, floating on the
   tinted background as a card. */
@media (min-width: {DESKTOP_BREAKPOINT}) {{
    .lk-page {{
        max-width: 560px;
        min-height: 0;
        margin: 32px auto;
        padding: 24px 24px;
        background-color: #ffffff;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    }}
}}
"""


def build_css() -> str:
    """Return the complete stylesheet for a generated page."""
    css = _BASE_CSS

    css += "\n.lk-profile {"
    css += "\n    display: flex;"
    css += "\n    flex-direction: column;"
    css += "\n    align-items: center;"
    css += "\n    gap: 16px;"
    css += "\n    padding-bottom: 16px;"
    css += "\n}"

    css += "\n.lk-name {"
    css += "\n    text-align: center;"
    css += "\n    width: 100%;"
    css += "\n}"
    css += "\n.lk-name-title {"
    css += "\n    margin: 0;"
    css += "\n    font-size: 24px;"
    css += "\n    font-weight: 700;"
    css += "\n}"
    css += "\n.lk-name-subtitle {"
    css += "\n    margin: 4px 0 0;"
    css += "\n    font-size: 14px;"
    css += "\n    font-weight: 400;"
    css += "\n    opacity: 0.8;"
    css += "\n}"
    css += "\n.lk-logo {"
    css += "\n    width: 96px;"
    css += "\n    height: 96px;"
    css += "\n    object-fit: cover;"
    css += "\n    border: 3px solid transparent;"
    css += "\n}"
    css += "\n.lk-logo-circle { border-radius: 50%; }"
    css += "\n.lk-logo-square { border-radius: 0; }"
    css += "\n.lk-bio {"
    css += "\n    margin: 0;"
    css += "\n    padding: 12px 20px;"
    css += "\n    font-size: 14px;"
    css += "\n    line-height: 1.6;"
    css += "\n    width: 100%;"
    css += "\n    border: 1px solid transparent;"
    css += "\n}"
    css += "\n.lk-cover {"
    css += "\n    width: 100%;"
    css += "\n    overflow: hidden;"
    css += "\n}"
    css += "\n.lk-cover-img {"
    css += "\n    width: 100%;"
    css += "\n    height: 160px;"
    css += "\n    object-fit: cover;"
    css += "\n    display: block;"
    css += "\n}"
    css += "\n.lk-cover-rounded .lk-cover-img {"
    css += "\n    border-radius: 16px;"
    css += "\n}"
    css += "\n.lk-title {"
    css += "\n    margin: 8px 0 0;"
    css += "\n    font-size: 28px;"
    css += "\n    font-weight: 700;"
    css += "\n    line-height: 1.3;"
    css += "\n    width: 100%;"
    css += "\n}"

    for name, radius in LINK_SHAPES.items():
        css += f"\n.lk-shape-{name} {{ border-radius: {radius}; }}"

    for name, alignment in LINK_ALIGNMENTS.items():
        css += f"\n.lk-align-{name} {{ justify-content: {alignment}; }}"

    return css + "\n"
