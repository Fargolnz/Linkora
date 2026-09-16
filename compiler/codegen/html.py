"""HTML generation for validated Linkora documents.

Every block type has a ``render_<block>`` function. The dispatch table at the
bottom of this module maps block names to their renderer, so adding a new
block requires registering a single new renderer.
"""

from __future__ import annotations

import calendar
import html
from urllib.parse import quote

from compiler.ast import Block, Document
from compiler.codegen.css import FONT_FAMILIES, build_css
from compiler.types import jalali_to_gregorian

from compiler.codegen.svg import (
    ADDRESS_META,
    CONTACT_META,
    DIVIDER_SVGS,
    NETWORK_META,
    PLATFORM_META,
    SUPERLINK_SVG,
    _icon_svg,
)


#: Counter used to give each slider block a unique HTML element id.
_slider_counter = 0

#: Inline script driving the Image slider dots: highlights the dot of the
#: slide currently in view and makes each dot jump to its slide.
SLIDER_JS = """<script>
(function () {
  var sliders = document.querySelectorAll('.lk-image-slider');
  if (!sliders.length) return;
  sliders.forEach(function (slider) {
    var track = slider.querySelector('.lk-image-slider-track');
    var dots = slider.querySelectorAll('.lk-image-slider-dot');
    if (!track || !dots.length) return;
    var current = -1;
    function slideIndex() {
      var width = track.clientWidth || 1;
      return Math.max(0, Math.min(dots.length - 1, Math.round(track.scrollLeft / width)));
    }
    function update() {
      var index = slideIndex();
      if (index === current) return;
      current = index;
      dots.forEach(function (dot, i) {
        dot.classList.toggle('is-active', i === current);
      });
    }
    dots.forEach(function (dot) {
      dot.addEventListener('click', function () {
        var i = Number(dot.getAttribute('data-slide'));
        track.scrollTo({ left: i * track.clientWidth, behavior: 'smooth' });
      });
    });
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  });
})();
</script>"""


#: Inline script driving the FAQ accordion. Clicking a question smoothly
#: animates the height of its answer open or closed. Each item toggles
#: independently, and the chevron is rotated to match the open state.
FAQ_JS = """<script>
(function () {
  document.querySelectorAll('.lk-faqitem').forEach(function (item) {
    var button = item.querySelector('.lk-faqitem-summary');
    var wrap = item.querySelector('.lk-faqitem-answer-wrap');
    if (!button || !wrap) return;
    var a11y = button.getAttribute('aria-expanded');
    // Start collapsed unless the item was rendered open.
    if (a11y === 'true') {
      wrap.style.height = wrap.scrollHeight + 'px';
    } else {
      wrap.style.height = '0px';
    }
    button.addEventListener('click', function () {
      var open = wrap.style.height !== '0px';
      if (open) {
        var from = wrap.scrollHeight;
        wrap.style.height = from + 'px';
        void wrap.offsetHeight;
        wrap.style.height = '0px';
        button.setAttribute('aria-expanded', 'false');
        item.classList.remove('is-open');
      } else {
        wrap.style.height = wrap.scrollHeight + 'px';
        button.setAttribute('aria-expanded', 'true');
        item.classList.add('is-open');
      }
    });
    if (window.ResizeObserver) {
      new ResizeObserver(function () {
        if (wrap.style.height !== '0px') {
          wrap.style.height = wrap.scrollHeight + 'px';
        }
      }).observe(wrap);
    }
  });
})();
</script>"""


#: Inline script driving live Countdown timers. Each countdown carries its
#: target epoch in a ``data-target`` attribute; a timer ticks every second,
#: updates the four digit boxes, freezes the boxes at zero on expiry, and then
#: reveals the optional ``expiredText`` message. Countdowns marked
#: ``data-digits="fa"`` render their numbers using Persian digits.
COUNTDOWN_JS = """<script>
(function () {
  var FA = {'0':'۰','1':'۱','2':'۲','3':'۳','4':'۴','5':'۵','6':'۶','7':'۷','8':'۸','9':'۹'};
  function pad(n, digits) {
    n = String(n);
    while (n.length < digits) n = '0' + n;
    return n;
  }
  function toPersian(s) {
    var out = '';
    for (var i = 0; i < s.length; i++) out += FA[s[i]] || s[i];
    return out;
  }
  function update(root) {
    var target = Number(root.getAttribute('data-target'));
    var now = Date.now();
    var diff = target - now;
    if (diff < 0) diff = 0;
    var days = Math.floor(diff / 86400000);
    var hours = Math.floor(diff % 86400000 / 3600000);
    var minutes = Math.floor(diff % 3600000 / 60000);
    var seconds = Math.floor(diff % 60000 / 1000);
    var vals = [pad(days, 2), pad(hours, 2), pad(minutes, 2), pad(seconds, 2)];
    var fa = root.getAttribute('data-digits') === 'fa';
    var boxes = root.querySelectorAll('.lk-countdown-digit');
    if (boxes.length === 4) {
      boxes.forEach(function (box, i) {
        box.textContent = fa ? toPersian(vals[i]) : vals[i];
      });
    }
    if (diff === 0) {
      var expired = root.querySelector('.lk-countdown-expired');
      if (expired) expired.style.display = 'block';
      if (root.__timer) { clearInterval(root.__timer); root.__timer = null; }
    }
  }
  document.querySelectorAll('.lk-countdown').forEach(function (root) {
    update(root);
    root.__timer = setInterval(function () { update(root); }, 1000);
  });
})();
</script>"""


def render_html(document: Document) -> str:
    """Render a validated document into a complete HTML page."""
    global _slider_counter, _faq_counter, _faq_item_counter, _countdown_counter
    _slider_counter = 0
    _faq_counter = 0
    _faq_item_counter = 0
    _countdown_counter = 0

    theme_block = next((b for b in document.blocks if b.name == "Theme"), None)
    theme_data = _theme_data(theme_block)
    content_blocks = [b for b in document.blocks if b.name != "Theme"]
    body = "\n".join(_render_block(block) for block in content_blocks)
    scripts = ""
    if _slider_counter > 0:
        scripts += SLIDER_JS + "\n"
    if _faq_counter > 0:
        scripts += FAQ_JS + "\n"
    if _countdown_counter > 0:
        scripts += COUNTDOWN_JS + "\n"

    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\">\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
        f"  {_theme_font_stylesheet_link(theme_data)}\n"
        "  <title>Linkora</title>\n"
        "  <style>\n"
        f"{build_css(theme_data)}"
        "  </style>\n"
        "</head>\n"
        "<body>\n"
        f"  <main class=\"lk-page\">\n{body}\n  </main>\n"
        f"{scripts}"
        "</body>\n"
        "</html>\n"
    )


_DEFAULT_FONT_STYLESHEET = (
    "https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700&display=swap"
)


def _theme_data(theme_block: Block | None) -> dict[str, str]:
    """Extract page-level theme values (background, backdrop, font)."""
    data: dict[str, str] = {}
    if theme_block is None:
        return data

    page_theme = next(
        (child for child in theme_block.children if child.name == "PageTheme"),
        None,
    )
    if page_theme is None:
        return data

    for target, src in (
        ("background", "backgroundColor"),
        ("backdrop", "backdropColor"),
        ("font", "fontFamily"),
    ):
        value = str(page_theme.resolved.get(src, ""))
        if value:
            data[target] = value
    return data


def _theme_font_stylesheet_link(theme_data: dict[str, str]) -> str:
    """Return the Google Fonts <link> URL for the active page font."""
    font = theme_data.get("font")
    if not font:
        return (
            f'<link href="{_DEFAULT_FONT_STYLESHEET}" rel="stylesheet">'
        )
    family = quote(FONT_FAMILIES.get(font, font), safe="")
    href = (
        "https://fonts.googleapis.com/css2?"
        f"family={family}:wght@400;600;700&display=swap"
    )
    return f'<link href="{href}" rel="stylesheet">'


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
    service = str(resolved["service"])
    meta = PLATFORM_META[service]

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
    shape = str(parent.get("shape", "rounded"))

    classes = " ".join(
        ["lk-socialitem", f"lk-shape-{shape}"]
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
        parts.append(f'<span class="lk-socialitem-title">{html.escape(title)}</span>')

    inner = "".join(parts)
    return (
        f'    <a class="{classes}" style="{style}" '
        f'href="{html.escape(url, quote=True)}">{inner}</a>'
    )


def render_socialmedia(block: Block) -> str:
    """Render a SocialMedia container as a responsive grid of items."""
    resolved = block.resolved
    columns = int(resolved["columns"])
    direction = str(resolved["direction"])

    items = "\n".join(_render_block(child) for child in block.children)
    return (
        f'  <section class="lk-social" '
        f'data-columns="{columns}" data-direction="{direction}">\n'
        f"{items}\n"
        f"  </section>"
    )


def render_socialnetwork_item(block: Block) -> str:
    """Render a single SocialNetwork item as a clickable styled button."""
    resolved = block.resolved
    parent = _parent_resolved(block)
    service = str(resolved["service"])
    meta = NETWORK_META[service]

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
    title_color = inherit("titleColor", "titleColor", "#3B3B3B")
    background_color = inherit("backgroundColor", "backgroundColor", meta["bg"])
    border_color = inherit("borderColor", "borderColor", "transparent")
    icon_color = str(resolved["iconColor"]) or str(parent.get("iconColor", "")) or ""

    show_title = bool(parent.get("showTitle", True))
    show_icon = bool(parent.get("showIcon", True))
    shape = str(parent.get("shape", "rounded"))

    classes = " ".join(
        ["lk-socialitem", f"lk-shape-{shape}"]
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
        parts.append(f'<span class="lk-socialitem-title">{html.escape(title)}</span>')

    inner = "".join(parts)
    return (
        f'    <a class="{classes}" style="{style}" '
        f'href="{html.escape(url, quote=True)}">{inner}</a>'
    )


def render_socialnetwork(block: Block) -> str:
    """Render a SocialNetwork container as a responsive grid of items."""
    resolved = block.resolved
    columns = int(resolved["columns"])
    direction = str(resolved["direction"])

    items = "\n".join(_render_block(child) for child in block.children)
    return (
        f'  <section class="lk-social" '
        f'data-columns="{columns}" data-direction="{direction}">\n'
        f"{items}\n"
        f"  </section>"
    )


def render_contact(block: Block) -> str:
    """Render a Contact container as a responsive grid of contact items."""
    resolved = block.resolved
    columns = int(resolved["columns"])
    direction = str(resolved["direction"])

    items = "\n".join(_render_block(child) for child in block.children)
    return (
        f'  <section class="lk-social" '
        f'data-columns="{columns}" data-direction="{direction}">\n'
        f"{items}\n"
        f"  </section>"
    )


def render_contact_item(block: Block) -> str:
    """Render a single Contact item as a clickable button with a scheme href."""
    resolved = block.resolved
    parent = _parent_resolved(block)
    service = str(resolved["service"])
    meta = CONTACT_META[service]

    def inherit(key: str, parent_key: str, fallback: str = "") -> str:
        value = str(resolved[key])
        if value:
            return value
        pvalue = str(parent.get(parent_key, ""))
        if pvalue:
            return pvalue
        return fallback

    title = str(resolved["title"]) or meta["name"]
    value = str(resolved["value"])
    title_color = inherit("titleColor", "titleColor", "#00B4B0")
    background_color = inherit("backgroundColor", "backgroundColor", meta["bg"])
    border_color = inherit("borderColor", "borderColor", "#00B4B0")
    icon_color = inherit("iconColor", "iconColor", "#00B4B0")

    show_title = bool(parent.get("showTitle", True))
    show_icon = bool(parent.get("showIcon", True))
    shape = str(parent.get("shape", "rounded"))

    classes = " ".join(
        ["lk-socialitem", f"lk-shape-{shape}"]
    )
    style = (
        f"color: {title_color}; "
        f"background-color: {background_color}; "
        f"border-color: {border_color};"
    )

    href = _contact_href(service, value)

    parts = []
    if show_icon:
        parts.append(_icon_svg(meta, icon_color))
    if show_title:
        parts.append(f'<span class="lk-socialitem-title">{html.escape(title)}</span>')

    inner = "".join(parts)
    return (
        f'    <a class="{classes}" style="{style}" '
        f'href="{html.escape(href, quote=True)}">{inner}</a>'
    )


def _contact_href(contact_type: str, value: str) -> str:
    """Build the destination href for a contact type from its raw value."""
    scheme = CONTACT_META[contact_type]["scheme"]
    if contact_type == "website":
        if "://" not in value:
            return scheme + value
        return value
    return scheme + value
def render_address(block: Block) -> str:
    """Render an Address container as an address caption plus a provider grid."""
    resolved = block.resolved
    columns = int(resolved["columns"])
    direction = str(resolved["direction"])
    address = str(resolved["address"])
    address_color = str(resolved["addressColor"]) or "#000000"

    items = "\n".join(_render_block(child) for child in block.children)
    caption = ""
    if address:
        caption = (
            f'  <div class="lk-address-caption" style="color: {address_color};">'
            f'{html.escape(address)}</div>\n'
        )
    return (
        f'  <section class="lk-social" '
        f'data-columns="{columns}" data-direction="{direction}">\n'
        f"{caption}"
        f"{items}\n"
        f"  </section>"
    )


def render_address_item(block: Block) -> str:
    """Render a single Address item as a clickable navigation button."""
    resolved = block.resolved
    parent = _parent_resolved(block)
    service = str(resolved["service"])
    meta = ADDRESS_META[service]

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
    title_color = inherit("titleColor", "titleColor", "#3B3B3B")
    background_color = inherit("backgroundColor", "backgroundColor", meta["bg"])
    border_color = inherit("borderColor", "borderColor", "transparent")
    icon_color = inherit("iconColor", "iconColor", "")

    show_title = bool(parent.get("showTitle", True))
    show_icon = bool(parent.get("showIcon", True))
    shape = str(parent.get("shape", "rounded"))

    classes = " ".join(
        ["lk-socialitem", f"lk-shape-{shape}"]
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
        parts.append(f'<span class="lk-socialitem-title">{html.escape(title)}</span>')

    inner = "".join(parts)
    return (
        f'    <a class="{classes}" style="{style}" '
        f'href="{html.escape(url, quote=True)}">{inner}</a>'
    )


def render_image(block: Block) -> str:
    """Render an Image container as a grid of cards or a slider carousel."""
    resolved = block.resolved
    display_mode = str(resolved["displayMode"])
    items = list(block.children)

    if display_mode == "slider":
        slider_id = _new_slider_id()
        image_shadow = bool(resolved.get("imageShadow", False))
        shape = str(resolved.get("shape") or "rounded")
        section_classes = ["lk-image", "lk-image-slider"]
        if image_shadow:
            section_classes.append("lk-imageslider--shadow")
            section_classes.append(f"lk-shape-{shape}")
        cards = []
        for i, child in enumerate(items):
            cards.append(
                _render_image_item(
                    child,
                    reserve_caption=False,
                    card_id=f"{slider_id}-slide-{i}",
                    apply_shadow=False,
                )
            )
        dots = []
        for i, child in enumerate(items):
            active = " is-active" if i == 0 else ""
            dots.append(
                f'      <button type="button" class="lk-image-slider-dot{active}" '
                f'data-slide="{i}" aria-label="Go to slide {i + 1}"></button>'
            )
        section_class = " ".join(section_classes)
        return (
            f'  <section class="{section_class}" id="{slider_id}">\n'
            f'    <div class="lk-image-slider-track">\n'
            + "\n".join(cards)
            + "\n"
            f'    </div>\n'
            f'    <div class="lk-image-slider-dots">\n'
            + "\n".join(dots)
            + "\n"
            f'    </div>\n'
            f"  </section>"
        )

    columns = int(resolved["columns"])
    direction = str(resolved["direction"])
    rows = []
    for i in range(0, len(items), columns):
        row_items = items[i : i + columns]
        has_caption = any(
            str(child.resolved.get("title") or "")
            or str(child.resolved.get("description") or "")
            for child in row_items
        )
        row_class = "lk-image-row--caption" if has_caption else "lk-image-row--plain"
        cards = "\n".join(
            _render_image_item(child, reserve_caption=has_caption)
            for child in row_items
        )
        rows.append(
            f'    <div class="lk-image-row {row_class}">\n{cards}\n    </div>'
        )
    body = "\n".join(rows)
    return (
        f'  <section class="lk-image lk-image-grid" data-direction="{direction}">\n'
        f"{body}\n"
        f"  </section>"
    )


def render_image_item(block: Block) -> str:
    """Render a single Image item as a display card (image + optional caption)."""
    return _render_image_item(block, reserve_caption=False)


def _new_slider_id() -> str:
    """Return a page-unique element id for a slider block."""
    global _slider_counter
    _slider_counter += 1
    return f"lk-slider-{_slider_counter}"


def _render_image_item(block: Block, reserve_caption: bool, card_id: str | None = None, *, apply_shadow: bool = True) -> str:
    """Render a single Image item as a display card.

    When ``reserve_caption`` is True the caption area is emitted even for
    cards without their own caption, reserving equal space across the row.
    ``card_id`` optionally adds an element id (used by slider slides).
    """
    resolved = block.resolved
    parent = _parent_resolved(block)
    image = str(resolved["image"])
    title = str(resolved["title"])
    description = str(resolved["description"])
    alt = str(resolved["alt"]) or title or description or "Image"
    shape = str(parent.get("shape", "rounded"))
    image_shadow = bool(parent.get("imageShadow", False))

    def inherit(key: str, parent_key: str) -> str:
        value = str(resolved[key])
        if value:
            return value
        return str(parent.get(parent_key, ""))

    background_color = inherit("backgroundColor", "backgroundColor") or "#FFFFFF"
    border_color = inherit("borderColor", "borderColor") or "transparent"
    title_color = (
        inherit("titleColor", "titleColor") or str(parent.get("titleColor", "#000000"))
    )
    description_color = (
        inherit("descriptionColor", "descriptionColor")
        or str(parent.get("descriptionColor", "#3B3B3B"))
    )

    has_caption = bool(title or description)
    classes = ["lk-imagecard", f"lk-shape-{shape}"]
    if has_caption:
        classes.append("lk-imagecard--has-caption")
    if apply_shadow and image_shadow:
        classes.append("lk-imagecard--shadow")

    style = (
        f"background-color: {background_color}; "
        f"border-color: {border_color};"
    )

    caption = ""
    if has_caption or reserve_caption:
        cap_parts = []
        if title:
            cap_parts.append(
                f'<div class="lk-imagecard-title" style="color: {title_color};">'
                f"{html.escape(title)}</div>"
            )
        if description:
            cap_parts.append(
                f'<div class="lk-imagecard-desc" style="color: {description_color};">'
                f"{html.escape(description)}</div>"
            )
        if cap_parts:
            inner = "\n        ".join(cap_parts)
            caption = (
                "\n      <figcaption class=\"lk-imagecard-caption\">\n        "
                + inner
                + "\n      </figcaption>"
            )
        else:
            caption = '\n      <figcaption class="lk-imagecard-caption lk-imagecard-caption--empty"></figcaption>'

    media = (
        f'\n      <img class="lk-imagecard-img lk-shape-{shape}" '
        f'src="{html.escape(image, quote=True)}" '
        f'alt="{html.escape(alt, quote=True)}">'
    )
    id_attr = f' id="{html.escape(card_id, quote=True)}"' if card_id else ""
    return (
        f'      <figure class="{" ".join(classes)}"{id_attr} style="{style}">'
        f"{media}{caption}"
        f"\n      </figure>"
    )


def render_banner(block: Block) -> str:
    """Render a Banner container as a grid of linked image cards."""
    resolved = block.resolved
    columns = int(resolved["columns"])
    direction = str(resolved["direction"])
    items = list(block.children)

    rows = []
    for i in range(0, len(items), columns):
        row_items = items[i : i + columns]
        cards = "\n".join(_render_banner_item(child) for child in row_items)
        rows.append(f'    <div class="lk-banner-row">\n{cards}\n    </div>')
    body = "\n".join(rows)
    return (
        f'  <section class="lk-banner" data-direction="{direction}">\n'
        f"{body}\n"
        f"  </section>"
    )


def _render_banner_item(block: Block) -> str:
    """Render a single Banner item as a linked image card with overlay."""
    resolved = block.resolved
    parent = _parent_resolved(block)
    image = str(resolved["image"])
    url = str(resolved["url"])
    title = str(resolved["title"])
    description = str(resolved["description"])
    alt = title or description or "Banner"
    shape = str(parent.get("shape", "rounded"))

    def inherit(key: str, parent_key: str) -> str:
        value = str(resolved[key])
        if value:
            return value
        return str(parent.get(parent_key, ""))

    border_color = inherit("borderColor", "borderColor") or "transparent"
    title_color = inherit("titleColor", "titleColor") or "#FFFFFF"
    description_color = (
        inherit("descriptionColor", "descriptionColor") or "#FFFFFF"
    )

    classes = " ".join(["lk-banneritem", f"lk-shape-{shape}"])
    style = f"border-color: {border_color};"

    title_html = ""
    if title:
        title_html = (
            f'\n      <div class="lk-banneritem-title" '
            f'style="color: {title_color};">'
            f"{html.escape(title)}</div>"
        )
    desc_html = ""
    if description:
        desc_html = (
            f'\n      <div class="lk-banneritem-desc" '
            f'style="color: {description_color};">'
            f"{html.escape(description)}</div>"
        )

    mask = f'\n    <div class="lk-banneritem-mask">{title_html}{desc_html}\n    </div>'
    img = (
        f'\n    <img class="lk-banneritem-img" '
        f'src="{html.escape(image, quote=True)}" '
        f'alt="{html.escape(alt, quote=True)}">'
    )
    return (
        f'    <a class="{classes}" href="{html.escape(url, quote=True)}" '
        f'style="{style}">'
        f"{img}{mask}"
        f"\n    </a>"
    )


def render_banner_item(block: Block) -> str:
    """Render a BannerItem — always rendered inside its container."""
    return _render_banner_item(block)


def _is_youtube_url(url: str) -> bool:
    """Return True if *url* is a YouTube watch URL and extract the video ID."""
    import re
    m = re.match(
        r"^https?://(?:(?:www\.)?youtube\.com/watch\?.*v=|youtu\.be/)([A-Za-z0-9_-]+)",
        url,
    )
    return m is not None


def _youtube_video_id(url: str) -> str:
    """Extract the YouTube video ID from a watch URL."""
    import re
    m = re.match(
        r"^https?://(?:(?:www\.)?youtube\.com/watch\?.*v=|youtu\.be/)([A-Za-z0-9_-]+)",
        url,
    )
    return m.group(1) if m else ""


def _is_aparat_url(url: str) -> bool:
    """Return True if *url* is an Aparat watch URL."""
    import re
    return bool(re.match(r"^https?://(?:www\.)?aparat\.com/v/[A-Za-z0-9_-]+", url))


def _is_local_video(url: str) -> bool:
    """Return True if *url* looks like a local video file path."""
    lower = url.lower()
    return any(lower.endswith(ext) for ext in (".mp4", ".webm", ".mov"))


def render_video(block: Block) -> str:
    """Render a Video block as a thumbnail card with play icon overlay."""
    resolved = block.resolved
    url = str(resolved["url"])
    thumbnail = str(resolved["thumbnail"])
    shape = str(resolved["shape"])
    border_color = str(resolved["borderColor"])

    is_yt = _is_youtube_url(url)
    is_ap = _is_aparat_url(url)
    is_local = _is_local_video(url)

    if not thumbnail and is_yt:
        vid = _youtube_video_id(url)
        thumbnail = f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"

    alt = "Video"
    style = f"border-color: {border_color};" if border_color != "transparent" else ""

    img_tag = (
        f'\n    <img class="lk-video-img" '
        f'src="{html.escape(thumbnail, quote=True)}" '
        f'alt="{html.escape(alt, quote=True)}">'
    ) if thumbnail else ""

    card_class = "lk-video" if thumbnail else "lk-video lk-video-no-thumbnail"

    play_icon = (
        '\n    <div class="lk-video-play">'
        '<div class="lk-video-play-triangle"></div>'
        '</div>'
    )

    inner = f"{img_tag}{play_icon}"

    if is_local:
        tag_open = (
            f'  <div class="{card_class} lk-shape-{shape}"'
            f'{f" style=\"{style}\"" if style else ""}>'
        )
        tag_close = "  </div>"
        video_el = (
            f'\n    <video class="lk-video-player" controls preload="metadata"'
            f' src="{html.escape(url, quote=True)}"></video>'
        )
        return f"{tag_open}{inner}{video_el}\n{tag_close}"

    tag_open = (
        f'  <a class="{card_class} lk-shape-{shape}" '
        f'href="{html.escape(url, quote=True)}" '
        f'target="_blank" rel="noopener"'
        f'{f" style=\"{style}\"" if style else ""}>'
    )
    tag_close = "  </a>"
    return f"{tag_open}{inner}\n{tag_close}"


_COUNTDOWN_UNITS = {
    "fa": ("روز", "ساعت", "دقیقه", "ثانیه"),
    "en": ("Days", "Hours", "Minutes", "Seconds"),
}


def render_countdown(block: Block) -> str:
    """Render a Countdown block as a live four-box timer.

    Each box shows one unit (days, hours, minutes, seconds) with a label
    underneath. The target moment is emitted as an epoch-millisecond
    ``data-target`` attribute consumed by the shared ``COUNTDOWN_JS`` script.
    """
    global _countdown_counter
    _countdown_counter += 1
    resolved = block.resolved
    date = str(resolved["date"])
    time = str(resolved["time"])
    expired_text = str(resolved["expiredText"])
    language = str(resolved["language"])
    calendar_name = str(resolved["calendar"])
    text_color = str(resolved["textColor"])
    background_color = str(resolved["backgroundColor"])
    border_color = str(resolved["borderColor"])
    shape = str(resolved["shape"])

    year, month, day = (int(part) for part in date.split("/"))
    hour, minute = (int(part) for part in time.split(":"))
    if calendar_name == "jalali":
        year, month, day = jalali_to_gregorian(year, month, day)
    target_ms = calendar.timegm(
        (year, month, day, hour, minute, 0, 0, 0, -1)
    ) * 1000

    style_parts = []
    if text_color and text_color != "transparent":
        style_parts.append(f"color: {text_color};")
    if background_color and background_color != "transparent":
        style_parts.append(f"background: {background_color};")
    if border_color and border_color != "transparent":
        style_parts.append(f"border-color: {border_color};")
    style = " ".join(style_parts)

    units = _COUNTDOWN_UNITS.get(language, _COUNTDOWN_UNITS["en"])
    persian_digits = language == "fa"
    initial_digit = "۰۰" if persian_digits else "00"
    digits_attr = ' data-digits="fa"' if persian_digits else ""
    boxes = "\n".join(
        '      <div class="lk-countdown-box">\n'
        f'        <span class="lk-countdown-digit">{initial_digit}</span>\n'
        f'        <span class="lk-countdown-label">{html.escape(label)}</span>\n'
        "      </div>"
        for label in units
    )

    expired = (
        f'\n      <div class="lk-countdown-expired" '
        f'style="display:none;">{html.escape(expired_text)}</div>'
        if expired_text
        else ""
    )

    card_class = "lk-countdown"
    if not background_color or background_color == "transparent":
        card_class += " lk-countdown-transparent"

    return (
        f'  <div class="{card_class} lk-shape-{shape}" '
        f'data-target="{target_ms}"{digits_attr}'
        f'{f" style=\"{style}\"" if style else ""}>'
        f'\n    <div class="lk-countdown-row">\n{boxes}\n    </div>'
        f"{expired}\n  </div>"
    )


def render_faq(block: Block) -> str:
    """Render an FAQ container as a list of accordion items."""
    global _faq_counter
    _faq_counter += 1
    items = "\n".join(_render_faq_item(child) for child in block.children)
    direction = str(block.resolved["direction"])
    return (
        f'  <div class="lk-faq" data-direction="{direction}">\n'
        f"{items}\n"
        f"  </div>"
    )


def render_faq_item(block: Block) -> str:
    """Render a single FAQ item as an animated accordion entry."""
    return _render_faq_item(block)


_faq_item_counter = 0


def _render_faq_item(block: Block) -> str:
    """Render a single FAQ item, inheriting colors from its container."""
    global _faq_item_counter
    _faq_item_counter += 1
    resolved = block.resolved
    parent = _parent_resolved(block)
    question = str(resolved["question"])
    answer = str(resolved["answer"])

    def inherit(key: str, parent_key: str, default: str = "") -> str:
        value = str(resolved[key])
        if value:
            return value
        return str(parent.get(parent_key, default)) or default

    question_color = inherit("questionColor", "questionColor", "#00B4B0")
    answer_color = inherit("answerColor", "answerColor", "#3B3B3B")
    icon_color = inherit("iconColor", "iconColor", "#00B4B0")
    background_color = inherit("backgroundColor", "backgroundColor", "#FFFFFF")
    border_color = inherit("borderColor", "borderColor", "#00B4B0")
    shape = str(parent.get("shape", "rounded")) or "rounded"

    style = (
        f"background-color: {background_color}; "
        f"border-color: {border_color};"
    )

    arrow_svg = (
        '<svg class="lk-faqitem-arrow" viewBox="0 0 24 24" aria-hidden="true">'
        f'<path fill="{html.escape(icon_color, quote=True)}" '
        'd="M5.59 7.41 10 11.83l4.41-4.42L16 8.83 10 14.83 4 8.83z"/>'
        "</svg>"
    )

    answer_id = f"lk-faqitem-answer-{_faq_item_counter}"
    return (
        f'    <div class="lk-faqitem lk-shape-{shape}" style="{style}">\n'
        f'      <button type="button" class="lk-faqitem-summary" '
        f'aria-expanded="false" aria-controls="{answer_id}">'
        f'<span class="lk-faqitem-question" style="color: {question_color};">'
        f"{html.escape(question)}</span>{arrow_svg}"
        f"</button>\n"
        f'      <div class="lk-faqitem-answer-wrap" id="{answer_id}">\n'
        f'        <div class="lk-faqitem-answer" style="color: {answer_color};">'
        f"{html.escape(answer)}</div>\n"
        f"      </div>\n"
        f"    </div>"
    )


def _parent_resolved(block: Block) -> dict[str, object]:
    """Return the resolved properties of the nearest ancestor block."""
    return block.parent.resolved if block.parent is not None else {}


def render_divider(block: Block) -> str:
    """Render a Divider block as an inline SVG ornament.

    The chosen style's artwork is emitted with every fill and stroke set to
    ``currentColor``, so the block's ``color`` property tints the divider via
    the wrapping element's ``color`` declaration. Vertical spacing is governed
    by ``marginTop`` and ``marginBottom``.
    """
    resolved = block.resolved
    style_name = str(resolved["style"])
    color = str(resolved["color"])
    margin_top = int(resolved["marginTop"])
    margin_bottom = int(resolved["marginBottom"])

    svg = DIVIDER_SVGS.get(style_name, DIVIDER_SVGS["orb"])
    style = (
        f"color: {color}; "
        f"margin-top: {margin_top}px; "
        f"margin-bottom: {margin_bottom}px;"
    )
    return (
        f'  <div class="lk-divider" style="{style}">\n'
        f"    {svg}\n"
        f"  </div>"
    )


def render_superlink(block: Block) -> str:
    """Render a SuperLink block as a prominent, multi-line link button.

    The button shows a title and optional description next to an icon. When no
    ``icon`` is supplied the built-in open-link SVG is used, filled with
    ``iconColor``. A user-supplied icon is left untouched unless ``iconColor``
    is explicitly given, in which case a CSS mask tints it to that color.

    The text stack is emitted before the icon so that, with the block's
    ``direction``, the text sits on the inline-start side and the icon on the
    inline-end side: ``ltr`` places the text left and the icon right, while
    ``rtl`` places the text right and the icon left.
    """
    resolved = block.resolved
    title = str(resolved["title"])
    description = str(resolved["description"])
    url = str(resolved["url"])
    icon = str(resolved["icon"])
    icon_color = str(resolved["iconColor"])
    shape = str(resolved["shape"])
    direction = str(resolved["direction"])
    title_color = str(resolved["titleColor"])
    description_color = str(resolved["descriptionColor"])
    background_color = str(resolved["backgroundColor"])
    border_color = str(resolved["borderColor"])

    if icon:
        if block.property("iconColor") is not None:
            icon_src = html.escape(icon, quote=True)
            icon_style = (
                f"-webkit-mask-image: url('{icon_src}'); "
                f"mask-image: url('{icon_src}'); "
                f"background-color: {icon_color};"
            )
            icon_html = f'    <span class="lk-superlink-icon lk-superlink-icon--tinted" style="{icon_style}" aria-hidden="true"></span>\n'
        else:
            icon_html = (
                f'    <img class="lk-superlink-icon" '
                f'src="{html.escape(icon, quote=True)}" alt="" aria-hidden="true">\n'
            )
    else:
        icon_html = (
            "    " + SUPERLINK_SVG.format(icon_color=icon_color) + "\n"
        )

    text_parts = [f'      <span class="lk-superlink-title" style="color: {title_color};">{html.escape(title)}</span>']
    if description:
        text_parts.append(
            f'      <span class="lk-superlink-desc" style="color: {description_color};">{html.escape(description)}</span>'
        )
    text_html = "\n".join(text_parts)

    classes = " ".join(["lk-superlink", f"lk-shape-{shape}"])
    style = (
        f"color: {title_color}; "
        f"background-color: {background_color}; "
        f"border-color: {border_color};"
    )

    return (
        f'  <a class="{classes}" style="{style}" '
        f'href="{html.escape(url, quote=True)}" '
        f'data-direction="{direction}">\n'
        f'    <div class="lk-superlink-text">\n'
        f"{text_html}\n"
        f"    </div>\n"
        f"{icon_html}"
        f"  </a>"
    )


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
    "SocialNetwork": render_socialnetwork,
    "SocialNetworkItem": render_socialnetwork_item,
    "Contact": render_contact,
    "ContactItem": render_contact_item,
    "Address": render_address,
    "AddressItem": render_address_item,
    "Image": render_image,
    "ImageItem": render_image_item,
    "Banner": render_banner,
    "BannerItem": render_banner_item,
    "Video": render_video,
    "Countdown": render_countdown,
    "FAQ": render_faq,
    "FAQItem": render_faq_item,
    "Divider": render_divider,
    "SuperLink": render_superlink,
}
