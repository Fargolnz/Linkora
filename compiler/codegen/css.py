"""Shared CSS for generated Linkora pages.

Block-specific CSS classes are named ``lk-<block>-<variant>`` so that new
blocks can reuse the same conventions without collisions.
"""

from __future__ import annotations

#: Border-radius (px) for each ``shape`` value shared by every block.
BLOCK_SHAPES = {
    "sharp": "0",
    "slightlyRounded": "6px",
    "rounded": "12px",
    "pill": "999px",
}

#: CSS flex alignment for each ``align`` value shared by every block.
BLOCK_ALIGNMENTS = {
    "left": "flex-start",
    "center": "center",
    "right": "flex-end",
}

#: Primary background of the page/card, identical on every screen size.
#: Overridable through a Theme block via the --lk-background variable.
BACKGROUND = "#ffffff"

#: Desktop-only surface behind the floating card, hidden on mobile where
#: the card fills the viewport. Overridable through a Theme block via
#: the --lk-backdrop variable.
BACKDROP = "#e0f4f4"

#: Default font stack. The lead family is swapped out when a Theme block
#: sets its own ``fontFamily``.
BASE_FONT_STACK = (
    '"Vazirmatn", -apple-system, BlinkMacSystemFont, "Segoe UI", '
    "Roboto, Helvetica, Arial, sans-serif"
)

#: Google Fonts family name for each ``PageTheme.fontFamily`` enum value.
#: The enum values are lowercase identifiers (per the Linkora grammar),
#: the mapping carries the properly-cased family name used in CSS.
FONT_FAMILIES = {
    "vazirmatn": "Vazirmatn",
    "inter": "Inter",
    "poppins": "Poppins",
    "rubik": "Rubik",
    "roboto": "Roboto",
}

#: Maps the camelCase DSL ``backgroundRepeat`` enum values to the CSS
#: ``background-repeat`` keyword they emit.
_REPEAT_CSS = {
    "repeat": "repeat",
    "noRepeat": "no-repeat",
    "repeatX": "repeat-x",
    "repeatY": "repeat-y",
}
_REPEAT_CSS_DEFAULT = "noRepeat"


#: Viewport width (px) above which the page becomes a floating card.
DESKTOP_BREAKPOINT = "600px"

#: Top-level block names whose markup needs the profile/text CSS group
#: (.lk-profile, .lk-name, .lk-logo, .lk-bio, .lk-cover, .lk-title, .lk-text).
_PROFILE_BLOCKS = frozenset(
    {"Profile", "Name", "Logo", "Bio", "Cover", "Title", "Text"}
)

#: Top-level block names whose markup needs the connect grid CSS group
#: (.lk-connect, .lk-address-caption, .lk-connectitem).
_CONNECT_BLOCKS = frozenset(
    {"SocialMedia", "SocialNetwork", "Contact", "Address"}
)

#: CSS group for each of the remaining blocks, keyed by top-level block name.
_LINK_BLOCKS = frozenset({"Link"})
_IMAGE_BLOCKS = frozenset({"Image"})
_BANNER_BLOCKS = frozenset({"Banner"})
_VIDEO_BLOCKS = frozenset({"Video"})
_FAQ_BLOCKS = frozenset({"FAQ"})
_SUPERLINK_BLOCKS = frozenset({"SuperLink"})
_COUNTDOWN_BLOCKS = frozenset({"Countdown"})
_DIVIDER_BLOCKS = frozenset({"Divider"})


def _css_wanted(used_blocks: set[str] | None, names: frozenset[str]) -> bool:
    """Return whether a CSS group should be emitted.

    A group is emitted when no block filter is supplied (``used_blocks`` is
    ``None``) or when the document uses at least one of ``names``.
    """
    return used_blocks is None or bool(used_blocks & names)


_BASE_CSS = """
:root {{
    color-scheme: light;
    --lk-background: {background};
    --lk-backdrop: {backdrop};
    --lk-background-image: {background_image};
    --lk-background-size: {background_size};
    --lk-background-repeat: {background_repeat};
    --lk-font-family: {font_family};
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
    font-family: var(--lk-font-family);
}}

/* Mobile-first: the page fills the phone viewport. */
.lk-page {{
    max-width: 100%;
    min-height: 100vh;
    min-height: 100dvh;
    margin: 0 auto;
    padding: 24px 16px;
    background-color: var(--lk-background);
    background-image: var(--lk-background-image);
    background-size: var(--lk-background-size);
    background-repeat: var(--lk-background-repeat);
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.lk-page * {{
    unicode-bidi: plaintext;
}}

/* Larger screens: a column slightly wider than a phone, floating on the
   tinted background as a card, centered with equal space above and below. */
@media (min-width: {desktop_breakpoint}) {{
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


def _utilities_css() -> str:
    """Shared shape and alignment utilities used by every block."""
    css = ""
    for name, radius in BLOCK_SHAPES.items():
        css += f"\n.lk-shape-{name} {{ border-radius: {radius}; }}"

    for name, alignment in BLOCK_ALIGNMENTS.items():
        css += f"\n.lk-align-{name} {{ justify-content: {alignment}; }}"
    return css


def _link_css() -> str:
    """Link button styling."""
    css = "\n.lk-link {"
    css += "\n    display: flex;"
    css += "\n    align-items: center;"
    css += "\n    width: 100%;"
    css += "\n    min-height: 52px;"
    css += "\n    padding: 16px 24px;"
    css += "\n    border: 2px solid transparent;"
    css += "\n    font-size: 16px;"
    css += "\n    font-weight: 600;"
    css += "\n    text-decoration: none;"
    css += "\n    transition: transform 120ms ease, opacity 120ms ease;"
    css += "\n}"
    css += "\n.lk-link:hover {"
    css += "\n    transform: translateY(-2px);"
    css += "\n    opacity: 0.92;"
    css += "\n}"
    return css


def _profile_css() -> str:
    """Profile identity + standalone text block styling."""
    css = "\n.lk-profile {"
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
    css += "\n    line-height: 1.5;"
    css += "\n}"
    css += "\n.lk-name-subtitle {"
    css += "\n    margin: 8px 0 0;"
    css += "\n    font-size: 14px;"
    css += "\n    line-height: 1.5;"
    css += "\n    font-weight: 400;"
    css += "\n    opacity: 0.8;"
    css += "\n}"
    css += "\n.lk-logo {"
    css += "\n    width: 96px;"
    css += "\n    height: 96px;"
    css += "\n    object-fit: cover;"
    css += "\n    border: 3px solid transparent;"
    css += "\n}"
    css += "\n.lk-bio,"
    css += "\n.lk-text {"
    css += "\n    margin: 0;"
    css += "\n    padding: 12px 0;"
    css += "\n    font-size: 14px;"
    css += "\n    line-height: 1.6;"
    css += "\n    width: 100%;"
    css += "\n    border: 1px solid transparent;"
    css += "\n}"
    css += "\n.lk-bio--boxed,"
    css += "\n.lk-text--boxed {"
    css += "\n    padding: 12px 20px;"
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
    css += "\n.lk-title {"
    css += "\n    margin: 32px 0 0;"
    css += "\n    font-size: 28px;"
    css += "\n    font-weight: 700;"
    css += "\n    line-height: 1.3;"
    css += "\n    width: 100%;"
    css += "\n}"
    return css


def _connect_css() -> str:
    """Connect grid styling (shared by SocialMedia, SocialNetwork,
    Contact, and Address)."""
    css = "\n.lk-connect {"
    css += "\n    display: flex;"
    css += "\n    flex-wrap: wrap;"
    css += "\n    justify-content: center;"
    css += "\n    gap: 12px;"
    css += "\n    width: 100%;"
    css += "\n}"
    css += "\n.lk-connect .lk-connectitem { flex: 0 1 100%; }"
    css += "\n.lk-connect[data-columns='1'] .lk-connectitem { flex-basis: 100%; }"
    css += "\n.lk-connect[data-columns='2'] .lk-connectitem { flex-basis: calc((100% - 12px) / 2); }"
    css += "\n.lk-connect[data-columns='3'] .lk-connectitem { flex-basis: calc((100% - 24px) / 3); }"
    css += "\n.lk-connect[data-columns='4'] .lk-connectitem { flex-basis: calc((100% - 36px) / 4); }"
    css += "\n.lk-connect[data-direction='rtl'] { direction: rtl; }"
    css += "\n.lk-connect[data-direction='ltr'] { direction: ltr; }"
    css += "\n.lk-address-caption {"
    css += "\n    flex: 0 1 100%;"
    css += "\n    text-align: center;"
    css += "\n    font-size: 15px;"
    css += "\n    font-weight: 600;"
    css += "\n    margin-bottom: 12px;"
    css += "\n}"
    css += "\n.lk-connectitem {"
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
    css += "\n.lk-connectitem:hover {"
    css += "\n    transform: translateY(-2px);"
    css += "\n    opacity: 0.92;"
    css += "\n}"
    css += "\n.lk-connectitem-icon {"
    css += "\n    display: inline-flex;"
    css += "\n    width: 22px;"
    css += "\n    height: 22px;"
    css += "\n    flex: 0 0 auto;"
    css += "\n}"
    css += "\n.lk-connectitem-icon svg {"
    css += "\n    width: 100%;"
    css += "\n    height: 100%;"
    css += "\n    display: block;"
    css += "\n}"
    css += "\n.lk-connectitem-title {"
    css += "\n    font-size: 15px;"
    css += "\n    font-weight: 600;"
    css += "\n    min-width: 0;"
    css += "\n    white-space: nowrap;"
    css += "\n    overflow: hidden;"
    css += "\n    text-overflow: ellipsis;"
    css += "\n}"
    return css


def _image_css() -> str:
    """Image grid + slider + card styling."""
    css = "\n.lk-image {"
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
    css += "\n.lk-image-grid[data-direction='rtl'] { direction: rtl; }"
    css += "\n.lk-image-grid[data-direction='ltr'] { direction: ltr; }"
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
    css += "\n.lk-imagecard--shadow,"
    css += "\n.lk-image-slider--shadow {"
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
    css += "\n    overflow-x: auto;"
    css += "\n    scroll-snap-type: x mandatory;"
    css += "\n    scrollbar-width: none;"
    css += "\n}"
    css += "\n.lk-image-slider .lk-image-slider-track::-webkit-scrollbar {"
    css += "\n    display: none;"
    css += "\n}"
    css += "\n.lk-image-slider .lk-imagecard {"
    css += "\n    flex: 0 0 100%;"
    css += "\n    margin: 0;"
    css += "\n    scroll-snap-align: center;"
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
    css += "\n    box-sizing: border-box;"
    css += "\n    aspect-ratio: 1 / 1;"
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
    return css


def _banner_css() -> str:
    """Banner card + mask + grid styling."""
    css = "\n.lk-banner {"
    css += "\n    width: 100%;"
    css += "\n}"
    css += "\n.lk-banner[data-direction='rtl'] { direction: rtl; }"
    css += "\n.lk-banner[data-direction='ltr'] { direction: ltr; }"
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
    return css


def _video_css() -> str:
    """Video card + play icon styling."""
    css = "\n.lk-video {"
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
    css += "\n.lk-video-img,"
    css += "\n.lk-video-player {"
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
    return css


def _faq_css() -> str:
    """FAQ accordion styling."""
    css = "\n.lk-faq {"
    css += "\n    display: flex;"
    css += "\n    flex-direction: column;"
    css += "\n    gap: 12px;"
    css += "\n    width: 100%;"
    css += "\n}"
    css += "\n.lk-faq[data-direction='rtl'] { direction: rtl; }"
    css += "\n.lk-faq[data-direction='ltr'] { direction: ltr; }"
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
    css += "\n    text-align: start;"
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
    return css


def _superlink_css() -> str:
    """SuperLink button styling."""
    css = "\n.lk-superlink {"
    css += "\n    display: flex;"
    css += "\n    align-items: center;"
    css += "\n    justify-content: space-between;"
    css += "\n    width: 100%;"
    css += "\n    min-height: 72px;"
    css += "\n    padding: 16px 24px;"
    css += "\n    border: 2px solid transparent;"
    css += "\n    font-size: 16px;"
    css += "\n    font-weight: 600;"
    css += "\n    text-decoration: none;"
    css += "\n    transition: transform 120ms ease, opacity 120ms ease;"
    css += "\n    gap: 12px;"
    css += "\n}"
    css += "\n.lk-superlink:hover {"
    css += "\n    transform: translateY(-2px);"
    css += "\n    opacity: 0.92;"
    css += "\n}"
    css += "\n.lk-superlink[data-direction='rtl'] { direction: rtl; }"
    css += "\n.lk-superlink[data-direction='ltr'] { direction: ltr; }"
    css += "\n.lk-superlink-icon {"
    css += "\n    width: 24px;"
    css += "\n    height: 24px;"
    css += "\n    flex-shrink: 0;"
    css += "\n}"
    css += "\n.lk-superlink-icon--tinted {"
    css += "\n    display: inline-block;"
    css += "\n    -webkit-mask: center / contain no-repeat;"
    css += "\n    mask: center / contain no-repeat;"
    css += "\n}"
    css += "\n.lk-superlink-text {"
    css += "\n    display: flex;"
    css += "\n    flex-direction: column;"
    css += "\n    gap: 4px;"
    css += "\n    min-width: 0;"
    css += "\n}"
    css += "\n.lk-superlink-title {"
    css += "\n    font-size: 16px;"
    css += "\n    font-weight: 600;"
    css += "\n    line-height: 1.4;"
    css += "\n    text-align: start;"
    css += "\n}"
    css += "\n.lk-superlink-desc {"
    css += "\n    font-size: 13px;"
    css += "\n    font-weight: 400;"
    css += "\n    opacity: 0.85;"
    css += "\n    line-height: 1.4;"
    css += "\n    text-align: start;"
    css += "\n}"
    return css


def _countdown_css() -> str:
    """Countdown timer styling."""
    css = "\n.lk-countdown {"
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
    css += "\n    direction: ltr;"
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
    return css


def _divider_css() -> str:
    """Divider ornament styling."""
    css = "\n.lk-divider {"
    css += "\n    width: 100%;"
    css += "\n    line-height: 0;"
    css += "\n    text-align: center;"
    css += "\n}"
    css += "\n.lk-divider-svg {"
    css += "\n    width: 100%;"
    css += "\n    height: auto;"
    css += "\n    display: inline-block;"
    css += "\n    vertical-align: middle;"
    css += "\n}"
    return css


def build_css(
    theme_data: dict[str, str] | None = None,
    used_blocks: set[str] | None = None,
) -> str:
    """Return the complete stylesheet for a generated page.

    ``theme_data`` optionally carries the page background, the desktop
    backdrop color, the page background image (with optional size,
    repeat, and position), and the page font family read from a Theme
    block. Every omitted key falls back to the built-in default.

    ``used_blocks`` optionally names the top-level blocks present in the
    document; when provided, only the CSS groups those blocks need are
    emitted. When ``None``, the full stylesheet is returned.
    """
    theme_data = theme_data or {}
    background = theme_data.get("background", BACKGROUND)
    backdrop = theme_data.get("backdrop", BACKDROP)
    background_image = theme_data.get("background_image", "none")
    if background_image and background_image != "none":
        background_image = f'url("{background_image}")'
    background_size = theme_data.get("background_size", "cover")
    background_repeat = _REPEAT_CSS.get(
        theme_data.get("background_repeat", _REPEAT_CSS_DEFAULT),
        _REPEAT_CSS[_REPEAT_CSS_DEFAULT],
    )
    font = theme_data.get("font")
    if font:
        font_family = (
            f'"{FONT_FAMILIES.get(font, font)}", -apple-system, '
            'BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
        )
    else:
        font_family = BASE_FONT_STACK

    css = _BASE_CSS.format(
        background=background,
        backdrop=backdrop,
        background_image=background_image,
        background_size=background_size,
        background_repeat=background_repeat,
        font_family=font_family,
        desktop_breakpoint=DESKTOP_BREAKPOINT,
    )

    css += _utilities_css()
    if _css_wanted(used_blocks, _LINK_BLOCKS):
        css += _link_css()
    if _css_wanted(used_blocks, _PROFILE_BLOCKS):
        css += _profile_css()
    if _css_wanted(used_blocks, _CONNECT_BLOCKS):
        css += _connect_css()
    if _css_wanted(used_blocks, _IMAGE_BLOCKS):
        css += _image_css()
    if _css_wanted(used_blocks, _BANNER_BLOCKS):
        css += _banner_css()
    if _css_wanted(used_blocks, _VIDEO_BLOCKS):
        css += _video_css()
    if _css_wanted(used_blocks, _FAQ_BLOCKS):
        css += _faq_css()
    if _css_wanted(used_blocks, _SUPERLINK_BLOCKS):
        css += _superlink_css()
    if _css_wanted(used_blocks, _COUNTDOWN_BLOCKS):
        css += _countdown_css()
    if _css_wanted(used_blocks, _DIVIDER_BLOCKS):
        css += _divider_css()
    return css + "\n"
