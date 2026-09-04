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

#: Primary background of the page/card, identical on every screen size.
#: Overridable later through a Theme block via the --lk-background
#: variable.
BACKGROUND = "#ffffff"

#: Desktop-only surface behind the floating card, hidden on mobile where
#: the card fills the viewport. Overridable later through a Theme block
#: via the --lk-backdrop variable.
BACKDROP = "#e0f4f4"

#: Viewport width (px) above which the page becomes a floating card.
DESKTOP_BREAKPOINT = "600px"

_BASE_CSS = f"""
:root {{
    color-scheme: light;
    --lk-background: {BACKGROUND};
    --lk-backdrop: {BACKDROP};
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
    background-color: var(--lk-backdrop);
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
    background-color: var(--lk-background);
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
   tinted background as a card, centered with equal space above and below. */
@media (min-width: {DESKTOP_BREAKPOINT}) {{
    body {{
        display: flex;
    }}

    .lk-page {{
        max-width: 560px;
        min-height: 0;
        margin: auto;
        padding: 24px 24px;
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
    css += "\n.lk-text {"
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

    # Social grid + item styling (shared by SocialMedia and SocialNetwork).
    css += "\n.lk-social {"
    css += "\n    display: grid;"
    css += "\n    gap: 12px;"
    css += "\n    width: 100%;"
    css += "\n}"
    css += "\n.lk-social[data-columns='1'] { grid-template-columns: 1fr; }"
    css += "\n.lk-social[data-columns='2'] { grid-template-columns: repeat(2, 1fr); }"
    css += "\n.lk-social[data-columns='3'] { grid-template-columns: repeat(3, 1fr); }"
    css += "\n.lk-social[data-columns='4'] { grid-template-columns: repeat(4, 1fr); }"
    css += "\n.lk-social[data-order='rtl'] { direction: rtl; }"
    css += "\n.lk-social[data-order='ltr'] { direction: ltr; }"
    css += "\n.lk-address-caption {"
    css += "\n    grid-column: 1 / -1;"
    css += "\n    text-align: center;"
    css += "\n    font-size: 15px;"
    css += "\n    font-weight: 600;"
    css += "\n    margin-bottom: 12px;"
    css += "\n}"
    css += "\n.lk-socialitem {"
    css += "\n    display: flex;"
    css += "\n    align-items: center;"
    css += "\n    justify-content: center;"
    css += "\n    gap: 8px;"
    css += "\n    min-height: 52px;"
    css += "\n    min-width: 0;"
    css += "\n    padding: 12px 12px;"
    css += "\n    border: 2px solid transparent;"
    css += "\n    text-decoration: none;"
    css += "\n    transition: transform 120ms ease, opacity 120ms ease;"
    css += "\n}"
    css += "\n.lk-socialitem:hover {"
    css += "\n    transform: translateY(-2px);"
    css += "\n    opacity: 0.92;"
    css += "\n}"
    css += "\n.lk-socialitem-icon {"
    css += "\n    display: inline-flex;"
    css += "\n    width: 22px;"
    css += "\n    height: 22px;"
    css += "\n    flex: 0 0 auto;"
    css += "\n}"
    css += "\n.lk-socialitem-icon svg {"
    css += "\n    width: 100%;"
    css += "\n    height: 100%;"
    css += "\n    display: block;"
    css += "\n}"
    css += "\n.lk-socialitem-title {"
    css += "\n    font-size: 15px;"
    css += "\n    font-weight: 600;"
    css += "\n    min-width: 0;"
    css += "\n    white-space: nowrap;"
    css += "\n    overflow: hidden;"
    css += "\n    text-overflow: ellipsis;"
    css += "\n}"
    css += "\n.lk-icon-left { flex-direction: row; }"
    css += "\n.lk-icon-right { flex-direction: row-reverse; }"
    css += "\n.lk-icon-top { flex-direction: column; gap: 4px; }"
    css += "\n.lk-icon-top .lk-socialitem-title { white-space: normal; text-align: center; }"

    # Image grid + slider + card styling.
    css += "\n.lk-image {"
    css += "\n    width: 100%;"
    css += "\n}"
    css += "\n.lk-image-grid .lk-image-row {"
    css += "\n    display: flex;"
    css += "\n    gap: 12px;"
    css += "\n    align-items: stretch;"
    css += "\n    margin-bottom: 12px;"
    css += "\n}"
    css += "\n.lk-image-grid .lk-image-row:last-child {"
    css += "\n    margin-bottom: 0;"
    css += "\n}"
    css += "\n.lk-image-row .lk-imagecard {"
    css += "\n    flex: 1 1 0;"
    css += "\n    min-width: 0;"
    css += "\n    margin: 0;"
    css += "\n    padding: 0;"
    css += "\n    display: flex;"
    css += "\n    flex-direction: column;"
    css += "\n    background-color: #FFFFFF;"
    css += "\n    border: 2px solid transparent;"
    css += "\n}"
    css += "\n.lk-imagecard-img {"
    css += "\n    display: block;"
    css += "\n    width: 100%;"
    css += "\n    aspect-ratio: 4 / 3;"
    css += "\n    object-fit: cover;"
    css += "\n    flex: 0 0 auto;"
    css += "\n}"
    css += "\n.lk-imagecard--shadow .lk-imagecard-img {"
    css += "\n    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);"
    css += "\n}"
    css += "\n.lk-imagecard--has-caption .lk-imagecard-img {"
    css += "\n    border-bottom-left-radius: 0;"
    css += "\n    border-bottom-right-radius: 0;"
    css += "\n}"
    css += "\n.lk-imagecard-caption {"
    css += "\n    padding: 12px;"
    css += "\n    display: flex;"
    css += "\n    flex-direction: column;"
    css += "\n    gap: 4px;"
    css += "\n    min-height: 60px;"
    css += "\n}"
    css += "\n.lk-imagecard-caption--empty {"
    css += "\n    min-height: 60px;"
    css += "\n}"
    css += "\n.lk-imagecard-title {"
    css += "\n    font-size: 15px;"
    css += "\n    font-weight: 600;"
    css += "\n    line-height: 1.4;"
    css += "\n}"
    css += "\n.lk-imagecard-desc {"
    css += "\n    font-size: 13px;"
    css += "\n    line-height: 1.5;"
    css += "\n}"
    css += "\n.lk-image-slider {"
    css += "\n    position: relative;"
    css += "\n    overflow: hidden;"
    css += "\n}"
    css += "\n.lk-image-slider .lk-image-slider-track {"
    css += "\n    display: flex;"
    css += "\n    gap: 12px;"
    css += "\n    overflow-x: auto;"
    css += "\n    scroll-snap-type: x mandatory;"
    css += "\n    scrollbar-width: none;"
    css += "\n}"
    css += "\n.lk-image-slider .lk-image-slider-track::-webkit-scrollbar {"
    css += "\n    display: none;"
    css += "\n}"
    css += "\n.lk-image-slider .lk-imagecard {"
    css += "\n    flex: 0 0 calc(100% - 12px);"
    css += "\n    margin: 0;"
    css += "\n    scroll-snap-align: center;"
    css += "\n}"
    css += "\n.lk-image-slider .lk-image-slider-track .lk-imagecard:last-child {"
    css += "\n    flex-basis: 100%;"
    css += "\n}"
    css += "\n.lk-image-slider-dots {"
    css += "\n    position: absolute;"
    css += "\n    top: 0;"
    css += "\n    left: 0;"
    css += "\n    right: 0;"
    css += "\n    aspect-ratio: 4 / 3;"
    css += "\n    display: flex;"
    css += "\n    justify-content: center;"
    css += "\n    align-items: flex-end;"
    css += "\n    gap: 8px;"
    css += "\n    pointer-events: none;"
    css += "\n}"
    css += "\n.lk-image-slider-dot {"
    css += "\n    width: 10px;"
    css += "\n    height: 10px;"
    css += "\n    padding: 0;"
    css += "\n    margin: 0 0 14px;"
    css += "\n    border: 2px solid rgba(255, 255, 255, 0.95);"
    css += "\n    border-radius: 50%;"
    css += "\n    background: transparent;"
    css += "\n    cursor: pointer;"
    css += "\n    pointer-events: auto;"
    css += "\n    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);"
    css += "\n    transition: background-color 150ms ease;"
    css += "\n}"
    css += "\n.lk-image-slider-dot.is-active {"
    css += "\n    background: #FFFFFF;"
    css += "\n}"

    # Banner card + mask + grid styling.
    css += "\n.lk-banner {"
    css += "\n    width: 100%;"
    css += "\n}"
    css += "\n.lk-banner .lk-banner-row {"
    css += "\n    display: flex;"
    css += "\n    gap: 12px;"
    css += "\n    align-items: stretch;"
    css += "\n    margin-bottom: 12px;"
    css += "\n}"
    css += "\n.lk-banner .lk-banner-row:last-child {"
    css += "\n    margin-bottom: 0;"
    css += "\n}"
    css += "\n.lk-banner-row .lk-banneritem {"
    css += "\n    flex: 1 1 0;"
    css += "\n    min-width: 0;"
    css += "\n    margin: 0;"
    css += "\n    padding: 0;"
    css += "\n    position: relative;"
    css += "\n    overflow: hidden;"
    css += "\n    display: block;"
    css += "\n    text-decoration: none;"
    css += "\n    border: 2px solid transparent;"
    css += "\n    transition: transform 120ms ease, opacity 120ms ease;"
    css += "\n}"
    css += "\n.lk-banner-row .lk-banneritem:hover {"
    css += "\n    transform: translateY(-2px);"
    css += "\n    opacity: 0.92;"
    css += "\n}"
    css += "\n.lk-banneritem-img {"
    css += "\n    display: block;"
    css += "\n    width: 100%;"
    css += "\n    aspect-ratio: 16 / 9;"
    css += "\n    object-fit: cover;"
    css += "\n}"
    css += "\n.lk-banneritem-mask {"
    css += "\n    position: absolute;"
    css += "\n    bottom: 0;"
    css += "\n    left: 0;"
    css += "\n    right: 0;"
    css += "\n    background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));"
    css += "\n    padding: 16px;"
    css += "\n    display: flex;"
    css += "\n    flex-direction: column;"
    css += "\n    justify-content: flex-end;"
    css += "\n    gap: 4px;"
    css += "\n}"
    css += "\n.lk-banneritem-title {"
    css += "\n    font-size: 15px;"
    css += "\n    font-weight: 600;"
    css += "\n    line-height: 1.4;"
    css += "\n}"
    css += "\n.lk-banneritem-desc {"
    css += "\n    font-size: 13px;"
    css += "\n    line-height: 1.5;"
    css += "\n}"

    # Video card + play icon styling.
    css += "\n.lk-video {"
    css += "\n    display: block;"
    css += "\n    position: relative;"
    css += "\n    overflow: hidden;"
    css += "\n    margin: 0;"
    css += "\n    padding: 0;"
    css += "\n    border: 2px solid transparent;"
    css += "\n    text-decoration: none;"
    css += "\n    transition: transform 120ms ease, opacity 120ms ease;"
    css += "\n}"
    css += "\n.lk-video:hover {"
    css += "\n    transform: translateY(-2px);"
    css += "\n    opacity: 0.92;"
    css += "\n}"
    css += "\n.lk-video-img {"
    css += "\n    display: block;"
    css += "\n    width: 100%;"
    css += "\n    aspect-ratio: 16 / 9;"
    css += "\n    object-fit: cover;"
    css += "\n}"
    css += "\n.lk-video-no-thumbnail {"
    css += "\n    aspect-ratio: 16 / 9;"
    css += "\n    background: linear-gradient(135deg, #e0e0e0, #c8c8c8);"
    css += "\n}"
    css += "\n.lk-video-play {"
    css += "\n    position: absolute;"
    css += "\n    top: 50%;"
    css += "\n    left: 50%;"
    css += "\n    transform: translate(-50%, -50%);"
    css += "\n    width: 56px;"
    css += "\n    height: 56px;"
    css += "\n    background: rgba(0, 0, 0, 0.55);"
    css += "\n    border-radius: 50%;"
    css += "\n    display: flex;"
    css += "\n    align-items: center;"
    css += "\n    justify-content: center;"
    css += "\n    pointer-events: none;"
    css += "\n}"
    css += "\n.lk-video-play-triangle {"
    css += "\n    width: 0;"
    css += "\n    height: 0;"
    css += "\n    border-style: solid;"
    css += "\n    border-width: 10px 0 10px 18px;"
    css += "\n    border-color: transparent transparent transparent #FFFFFF;"
    css += "\n    margin-left: 4px;"
    css += "\n}"
    css += "\n.lk-video-player {"
    css += "\n    display: block;"
    css += "\n    width: 100%;"
    css += "\n    aspect-ratio: 16 / 9;"
    css += "\n    object-fit: cover;"
    css += "\n}"

    # FAQ accordion styling.
    css += "\n.lk-faq {"
    css += "\n    display: flex;"
    css += "\n    flex-direction: column;"
    css += "\n    gap: 12px;"
    css += "\n    width: 100%;"
    css += "\n}"
    css += "\n.lk-faqitem {"
    css += "\n    margin: 0;"
    css += "\n    padding: 0;"
    css += "\n    border: 2px solid;"
    css += "\n    overflow: hidden;"
    css += "\n}"
    css += "\n.lk-faqitem-summary {"
    css += "\n    appearance: none;"
    css += "\n    -webkit-appearance: none;"
    css += "\n    margin: 0;"
    css += "\n    padding: 16px;"
    css += "\n    border: 0;"
    css += "\n    background: transparent;"
    css += "\n    font-family: inherit;"
    css += "\n    color: inherit;"
    css += "\n    text-align: left;"
    css += "\n    width: 100%;"
    css += "\n    display: flex;"
    css += "\n    align-items: center;"
    css += "\n    justify-content: space-between;"
    css += "\n    gap: 16px;"
    css += "\n    cursor: pointer;"
    css += "\n    user-select: none;"
    css += "\n}"
    css += "\n.lk-faqitem-question {"
    css += "\n    font-size: 15px;"
    css += "\n    font-weight: 600;"
    css += "\n    line-height: 1.4;"
    css += "\n}"
    css += "\n.lk-faqitem-arrow {"
    css += "\n    width: 20px;"
    css += "\n    height: 20px;"
    css += "\n    flex-shrink: 0;"
    css += "\n    transition: transform 180ms ease;"
    css += "\n}"
    css += "\n.lk-faqitem.is-open .lk-faqitem-arrow {"
    css += "\n    transform: rotate(180deg);"
    css += "\n}"
    css += "\n.lk-faqitem-answer-wrap {"
    css += "\n    overflow: hidden;"
    css += "\n    height: 0;"
    css += "\n    transition: height 260ms ease;"
    css += "\n}"
    css += "\n.lk-faqitem-answer {"
    css += "\n    padding: 0 16px 16px;"
    css += "\n    font-size: 14px;"
    css += "\n    line-height: 1.6;"
    css += "\n}"

    # Countdown timer styling.
    css += "\n.lk-countdown {"
    css += "\n    width: 100%;"
    css += "\n    box-sizing: border-box;"
    css += "\n    border: 2px solid transparent;"
    css += "\n    padding: 20px 16px;"
    css += "\n    text-align: center;"
    css += "\n}"
    css += "\n.lk-countdown-transparent {"
    css += "\n    background: transparent;"
    css += "\n}"
    css += "\n.lk-countdown-row {"
    css += "\n    display: flex;"
    css += "\n    justify-content: center;"
    css += "\n    gap: 24px;"
    css += "\n}"
    css += "\n.lk-countdown-box {"
    css += "\n    display: flex;"
    css += "\n    flex-direction: column;"
    css += "\n    align-items: center;"
    css += "\n    min-width: 60px;"
    css += "\n}"
    css += "\n.lk-countdown-digit {"
    css += "\n    font-size: 32px;"
    css += "\n    font-weight: 700;"
    css += "\n    line-height: 1.2;"
    css += "\n    font-variant-numeric: tabular-nums;"
    css += "\n}"
    css += "\n.lk-countdown-label {"
    css += "\n    font-size: 12px;"
    css += "\n    opacity: 0.7;"
    css += "\n    margin-top: 4px;"
    css += "\n}"
    css += "\n.lk-countdown-expired {"
    css += "\n    margin-top: 12px;"
    css += "\n    font-size: 14px;"
    css += "\n    font-weight: 600;"
    css += "\n}"
    css += "\n@media (max-width: " + DESKTOP_BREAKPOINT + ") {"
    css += "\n    .lk-countdown-row {"
    css += "\n        gap: 16px;"
    css += "\n    }"
    css += "\n    .lk-countdown-digit {"
    css += "\n        font-size: 24px;"
    css += "\n    }"
    css += "\n}"

    return css + "\n"
