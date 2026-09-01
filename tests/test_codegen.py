"""Tests for HTML code generation."""

from __future__ import annotations

from tests.helpers import compile_ok

LINK = 'Link { title: "GitHub", url: "https://github.com" }'


def _html(source: str = LINK) -> str:
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
        assert "--lk-background: #ffffff" in html
        assert "--lk-backdrop: #e0f4f4" in html
        assert "background-color: var(--lk-background);" in html
        assert "background-color: var(--lk-backdrop);" in html

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

    def test_vazirmatn_font_loaded(self):
        html = _html()
        assert "https://fonts.googleapis.com/css2?family=Vazirmatn" in html
        assert '"Vazirmatn"' in html


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
            'Link { title: "Portfolio", url: "https://example.com", '
            'align: left, shape: pill, backgroundColor: "#3B82F6", '
            'titleColor: "#000000", borderColor: "#2563EB" }'
        )
        assert 'class="lk-link lk-shape-pill lk-align-left"' in html
        assert (
            'style="color: #000000; background-color: #3B82F6; '
            'border-color: #2563EB;"'
        ) in html

    def test_multiple_links_rendered_in_order(self):
        html = _html(
            'Link { title: "First", url: "https://a.com" }\n'
            'Link { title: "Second", url: "https://b.com" }\n'
        )
        first = html.index(">First</a>")
        second = html.index(">Second</a>")
        assert first < second

    def test_html_escaping(self):
        html = _html(
            'Link { title: "He said \\"Hi & Bye\\"", '
            'url: "https://x.com/?a=1&b=2" }'
        )
        assert "He said &quot;Hi &amp; Bye&quot;" in html
        assert 'href="https://x.com/?a=1&amp;b=2"' in html

    def test_newline_escape_rendered_as_newline(self):
        html = _html(
            'Link { title: "Line1\\nLine2", url: "https://x.com" }'
        )
        assert "Line1\nLine2" in html


class TestTitleRendering:
    def test_renders_heading(self):
        html = _html('Title { title: "My Links" }')
        assert (
            '<h2 class="lk-title" style="color: #000000; '
            'text-align: center;">My Links</h2>'
        ) in html

    def test_custom_visual_properties(self):
        html = _html(
            'Title { title: "Customized", align: left, titleColor: "#c7006e" }'
        )
        assert (
            '<h2 class="lk-title" style="color: #c7006e; '
            'text-align: left;">Customized</h2>'
        ) in html

    def test_html_escaping(self):
        html = _html('Title { title: "He said \\"Hi & Bye\\"" }')
        assert "He said &quot;Hi &amp; Bye&quot;" in html

    def test_multiple_titles_rendered_in_order(self):
        html = _html(
            'Title { title: "First" }\n'
            'Title { title: "Second" }\n'
        )
        first = html.index(">First</h2>")
        second = html.index(">Second</h2>")
        assert first < second

    def test_title_css_present(self):
        html = _html('Title { title: "My Links" }')
        assert ".lk-title" in html
        assert "font-size: 28px" in html


class TestTextRendering:
    def test_renders_paragraph(self):
        html = _html('Text { text: "Hello" }')
        assert (
            '<p class="lk-text lk-shape-rounded" '
            'style="color: #000000; background-color: transparent; '
            'border-color: transparent; text-align: center;">Hello</p>'
        ) in html

    def test_custom_visual_properties(self):
        html = _html(
            'Text { text: "Custom", align: left, textColor: "#333333", '
            'backgroundColor: "#F3F4F6", borderColor: "#2563EB", shape: pill }'
        )
        assert 'class="lk-text lk-shape-pill"' in html
        assert (
            'style="color: #333333; background-color: #F3F4F6; '
            'border-color: #2563EB; text-align: left;"'
        ) in html

    def test_html_escaping(self):
        html = _html('Text { text: "He said \\"Hi & Bye\\"" }')
        assert "He said &quot;Hi &amp; Bye&quot;" in html

    def test_multiple_texts_rendered_in_order(self):
        html = _html('Text { text: "First" }\nText { text: "Second" }\n')
        first = html.index(">First</p>")
        second = html.index(">Second</p>")
        assert first < second

    def test_text_css_present(self):
        html = _html('Text { text: "Hello" }')
        assert ".lk-text" in html
        assert "font-size: 14px" in html


PROFILE = (
    'Profile {\n'
    '    Cover { image: "https://x.com/cover.jpg" }\n'
    '    Logo { image: "https://x.com/photo.jpg" }\n'
    '    Name { title: "Fargol", subtitle: "Dev" }\n'
    '    Bio { text: "Building things" }\n'
    '}\n'
)


class TestProfileRendering:
    def test_profile_section(self):
        html = _html(PROFILE)
        assert '<section class="lk-profile">' in html
        assert "</section>" in html

    def test_cover_renders_first(self):
        html = _html(PROFILE)
        cover_pos = html.index('<div class="lk-cover')
        logo_pos = html.index('<img class="lk-logo')
        assert cover_pos < logo_pos

    def test_name_renders_after_logo(self):
        html = _html(PROFILE)
        logo_pos = html.index('<img class="lk-logo')
        name_pos = html.index('<div class="lk-name')
        assert logo_pos < name_pos

    def test_bio_renders_last(self):
        html = _html(PROFILE)
        name_pos = html.index("lk-name")
        bio_pos = html.index("lk-bio")
        assert name_pos < bio_pos

    def test_name_title_and_subtitle(self):
        html = _html(PROFILE)
        assert "Fargol" in html
        assert "Dev" in html
        assert "lk-name-title" in html
        assert "lk-name-subtitle" in html

    def test_logo_shape(self):
        html = _html(PROFILE)
        assert "lk-logo-circle" in html

    def test_cover_shape(self):
        html = _html(PROFILE)
        assert "lk-cover-rounded" in html

    def test_bio_text(self):
        html = _html(PROFILE)
        assert "Building things" in html

    def test_empty_profile(self):
        html = _html("Profile {}")
        assert '<section class="lk-profile">' in html


SOCIAL = (
    "SocialMedia {\n"
    "    SocialMediaItem { service: instagram, url: \"https://ig/insta\" }\n"
    "    SocialMediaItem { service: github, url: \"https://gh/me\" }\n"
    "}\n"
)


class TestSocialMediaRendering:
    def test_grid_section(self):
        html = _html(SOCIAL)
        assert '<section class="lk-social"' in html
        assert 'data-columns="1"' in html

    def test_item_anchor(self):
        html = _html(SOCIAL)
        assert 'class="lk-socialitem lk-shape-rounded lk-icon-right"' in html
        assert 'href="https://ig/insta"' in html

    def test_service_title_defaults_to_name(self):
        html = _html(SOCIAL)
        assert ">Instagram</span>" in html
        assert ">GitHub</span>" in html

    def test_brand_icon_present(self):
        html = _html(SOCIAL)
        assert 'class="lk-socialitem-icon"' in html

    def test_columns_attribute(self):
        html = _html(
            "SocialMedia {\n"
            "    columns: 2\n"
            "    SocialMediaItem { service: x, url: \"https://x.com\" }\n"
            "    SocialMediaItem { service: x, url: \"https://x.com\" }\n"
            "}\n"
        )
        assert 'data-columns="2"' in html

    def test_css_styles_present(self):
        html = _html(SOCIAL)
        assert ".lk-socialitem" in html
        assert "grid-template-columns: repeat(3, 1fr)" in html

    def test_item_shrinks_in_narrow_grid(self):
        html = _html(SOCIAL)
        assert "min-width: 0" in html
        assert "text-overflow: ellipsis" in html
        assert "white-space: nowrap" in html

    def test_instagram_icon_uses_gradient_fill(self):
        html = _html(SOCIAL)
        assert "linearGradient" in html
        assert 'fill="url(#ig)"' in html

    def test_brand_icons_use_exact_brand_hex(self):
        html = _html(
            "SocialMedia {\n"
            "    SocialMediaItem { service: github, url: \"https://gh/me\" }\n"
            "    SocialMediaItem { service: pinterest, url: \"https://pin/x\" }\n"
            "    SocialMediaItem { service: telegram, url: \"https://t/x\" }\n"
            "}\n"
        )
        assert 'fill="#181717"' in html  # GitHub
        assert 'fill="#BD081C"' in html  # Pinterest
        assert 'fill="#26A5E4"' in html  # Telegram

    def test_icon_color_recolors_gradient_and_flat_fills(self):
        html = _html(
            "SocialMedia {\n"
            "    iconColor: \"#123456\"\n"
            "    SocialMediaItem { service: instagram, url: \"https://ig/x\" }\n"
            "    SocialMediaItem { service: github, url: \"https://gh/me\" }\n"
            "}\n"
        )
        assert 'stop-color="#123456"' in html  # Instagram gradient stops
        assert 'fill="url(#ig)"' in html  # gradient fill reference preserved
        assert 'fill="#123456"' in html  # GitHub flat fill recolored


SOCIAL_NETWORK = (
    "SocialNetwork {\n"
    "    SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
    "    SocialNetworkItem { service: discord, url: \"https://discord.gg/x\" }\n"
    "}\n"
)


class TestSocialNetworkRendering:
    def test_grid_section(self):
        html = _html(SOCIAL_NETWORK)
        assert '<section class="lk-social"' in html
        assert 'data-columns="1"' in html

    def test_item_anchor(self):
        html = _html(SOCIAL_NETWORK)
        assert 'class="lk-socialitem lk-shape-rounded lk-icon-right"' in html
        assert 'href="https://wa.me/1"' in html

    def test_service_title_defaults_to_name(self):
        html = _html(SOCIAL_NETWORK)
        assert ">WhatsApp</span>" in html
        assert ">Discord</span>" in html

    def test_brand_icon_present(self):
        html = _html(SOCIAL_NETWORK)
        assert 'class="lk-socialitem-icon"' in html

    def test_columns_attribute(self):
        html = _html(
            "SocialNetwork {\n"
            "    columns: 2\n"
            "    SocialNetworkItem { service: telegram, url: \"https://t.me/x\" }\n"
            "    SocialNetworkItem { service: telegram, url: \"https://t.me/y\" }\n"
            "}\n"
        )
        assert 'data-columns="2"' in html

    def test_css_styles_present(self):
        html = _html(SOCIAL_NETWORK)
        assert ".lk-socialitem" in html
        assert "grid-template-columns: repeat(3, 1fr)" in html

    def test_item_shrinks_in_narrow_grid(self):
        html = _html(SOCIAL_NETWORK)
        assert "min-width: 0" in html
        assert "text-overflow: ellipsis" in html

    def test_brand_icons_use_exact_brand_hex(self):
        html = _html(
            "SocialNetwork {\n"
            "    SocialNetworkItem { service: telegram, url: \"https://t.me/x\" }\n"
            "    SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
            "    SocialNetworkItem { service: discord, url: \"https://d.gg/x\" }\n"
            "}\n"
        )
        assert 'fill="#0088CC"' in html  # Telegram
        assert 'fill="#25D366"' in html  # WhatsApp
        assert 'fill="#5865F2"' in html  # Discord

    def test_new_network_service_brand_hexes(self):
        html = _html(
            "SocialNetwork {\n"
            "    SocialNetworkItem { service: bale, url: \"https://ble.ir/x\" }\n"
            "    SocialNetworkItem { service: eitaa, url: \"https://eitaa.com/x\" }\n"
            "    SocialNetworkItem { service: rubika, url: \"https://rubika.ir/x\" }\n"
            "}\n"
        )
        assert 'fill="#0ACA9B"' in html  # Bale
        assert 'fill="#ee7f22"' in html  # Eitaa
        assert 'fill="#49BDCA"' in html  # Rubika
        assert 'fill="#0F68A0"' in html  # Rubika

    def test_default_title_color_is_3b3b3b(self):
        html = _html(SOCIAL_NETWORK)
        assert "color: #3B3B3B" in html


CONTACT = (
    "Contact {\n"
    "    ContactItem { service: email, value: \"hi@example.com\" }\n"
    "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
    "}\n"
)


class TestContactRendering:
    def test_grid_section(self):
        html = _html(CONTACT)
        assert '<section class="lk-social"' in html
        assert 'data-columns="1"' in html

    def test_item_anchor(self):
        html = _html(CONTACT)
        assert 'class="lk-socialitem lk-shape-rounded lk-icon-right"' in html

    def test_title_defaults_to_service_name(self):
        html = _html(CONTACT)
        assert ">Email</span>" in html
        assert ">Mobile</span>" in html

    def test_icon_present(self):
        html = _html(CONTACT)
        assert 'class="lk-socialitem-icon"' in html

    def test_columns_attribute(self):
        html = _html(
            "Contact {\n"
            "    columns: 2\n"
            "    ContactItem { service: email, value: \"hi@example.com\" }\n"
            "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
            "}\n"
        )
        assert 'data-columns="2"' in html

    def test_css_styles_present(self):
        html = _html(CONTACT)
        assert ".lk-socialitem" in html

    def test_href_mailto(self):
        html = _html(
            "Contact {\n"
            "    ContactItem { service: email, value: \"hi@example.com\" }\n"
            "}\n"
        )
        assert 'href="mailto:hi@example.com"' in html

    def test_href_tel(self):
        html = _html(
            "Contact {\n"
            "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
            "}\n"
        )
        assert 'href="tel:+1 234 567 8901"' in html

    def test_href_sms(self):
        html = _html(
            "Contact {\n"
            "    ContactItem { service: sms, value: \"+1 234 567 8901\" }\n"
            "}\n"
        )
        assert 'href="sms:+1 234 567 8901"' in html

    def test_href_website_with_scheme(self):
        html = _html(
            "Contact {\n"
            "    ContactItem { service: website, value: \"https://example.com\" }\n"
            "}\n"
        )
        assert 'href="https://example.com"' in html

    def test_href_website_without_scheme(self):
        html = _html(
            "Contact {\n"
            "    ContactItem { service: website, value: \"example.org\" }\n"
            "}\n"
        )
        assert 'href="https://example.org"' in html

    def test_default_title_color_is_00b4b0(self):
        html = _html(CONTACT)
        assert "color: #00B4B0" in html

    def test_icon_color_recolors_contact_icons(self):
        html = _html(
            "Contact {\n"
            "    iconColor: \"#123456\"\n"
            "    ContactItem { service: email, value: \"hi@example.com\" }\n"
            "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
            "}\n"
        )
        assert 'fill="#123456"' in html
        assert 'fill="#00B4B0"' not in html


ADDRESS = (
    "Address {\n"
    "    AddressItem { service: googleMap, url: \"https://maps.google.com/?q=T\" }\n"
    "    AddressItem { service: waze, url: \"https://waze.com/ul?q=T\" }\n"
    "}\n"
)


class TestAddressRendering:
    def test_grid_section(self):
        html = _html(ADDRESS)
        assert '<section class="lk-social"' in html
        assert 'data-columns="1"' in html

    def test_item_anchor_with_url_href(self):
        html = _html(ADDRESS)
        assert 'href="https://maps.google.com/?q=T"' in html
        assert 'href="https://waze.com/ul?q=T"' in html

    def test_title_defaults_to_service_name(self):
        html = _html(ADDRESS)
        assert ">Google Maps</span>" in html
        assert ">Waze</span>" in html

    def test_icon_present_with_brand_hexes(self):
        html = _html(ADDRESS)
        assert 'class="lk-socialitem-icon"' in html
        assert 'fill="#ea4335"' in html
        assert 'fill="#33CCFF"' in html

    def test_all_service_brand_hexes(self):
        html = _html(
            "Address {\n"
            "    AddressItem { service: googleMap, url: \"https://g/x\" }\n"
            "    AddressItem { service: waze, url: \"https://w/x\" }\n"
            "    AddressItem { service: neshan, url: \"https://n/x\" }\n"
            "    AddressItem { service: balad, url: \"https://b/x\" }\n"
            "}\n"
        )
        assert 'fill="#ea4335"' in html
        assert 'fill="#33CCFF"' in html
        assert 'fill="#10b990"' in html
        assert 'fill="#7868f6"' in html

    def test_default_background_is_per_service_shade(self):
        html = _html(ADDRESS)
        assert "background-color: #E8F0FE" in html
        assert "background-color: #E5F6FC" in html

    def test_default_border_is_transparent(self):
        html = _html(ADDRESS)
        assert "border-color: transparent" in html

    def test_default_title_color_is_3b3b3b(self):
        html = _html(ADDRESS)
        assert "color: #3B3B3B" in html

    def test_address_caption_rendered(self):
        html = _html(
            "Address {\n"
            "    address: \"Tehran, Iran\"\n"
            "    addressColor: \"#111111\"\n"
            "    AddressItem { service: googleMap, url: \"https://g/x\" }\n"
            "}\n"
        )
        assert "Tehran, Iran" in html
        assert "color: #111111" in html

    def test_no_caption_when_address_empty(self):
        html = _html(ADDRESS)
        assert "Tehran, Iran" not in html

    def test_icon_color_recolors_address_icons(self):
        html = _html(
            "Address {\n"
            "    iconColor: \"#123456\"\n"
            "    AddressItem { service: googleMap, url: \"https://g/x\" }\n"
            "}\n"
        )
        assert 'fill="#123456"' in html
        assert 'fill="#ea4335"' not in html

    def test_item_color_inheritance(self):
        html = _html(
            "Address {\n"
            "    titleColor: \"#FF0000\"\n"
            "    backgroundColor: \"#EEEEEE\"\n"
            "    AddressItem { service: googleMap, url: \"https://g/x\" }\n"
            "}\n"
        )
        assert "color: #FF0000" in html
        assert "background-color: #EEEEEE" in html


class TestImageRendering:
    SRC = (
        "Image {\n"
        "    ImageItem { image: \"./assets/one.jpg\" }\n"
        "    ImageItem { image: \"./assets/two.jpg\", title: \"Two\" }\n"
        "}\n"
    )

    def test_grid_section_and_rows(self):
        html = _html(self.SRC)
        assert '<section class="lk-image lk-image-grid">' in html
        assert 'class="lk-image-row lk-image-row--caption"' in html

    def test_card_and_image_alt(self):
        html = _html(self.SRC)
        assert 'class="lk-imagecard lk-shape-rounded lk-imagecard--has-caption"' in html
        assert 'src="./assets/one.jpg"' in html
        assert 'alt="Two"' in html
        assert 'alt="Image"' in html

    def test_caption_reserved_across_caption_row(self):
        html = _html(
            "Image {\n"
            "    columns: 2\n"
            "    ImageItem { image: \"./assets/one.jpg\" }\n"
            "    ImageItem { image: \"./assets/two.jpg\", title: \"Two\" }\n"
            "}\n"
        )
        assert 'class="lk-imagecard-caption lk-imagecard-caption--empty"' in html
        assert ">Two</div>" in html

    def test_captions_absent_in_plain_row(self):
        html = _html(
            "Image {\n"
            "    columns: 2\n"
            "    ImageItem { image: \"./assets/one.jpg\" }\n"
            "    ImageItem { image: \"./assets/two.jpg\" }\n"
            "}\n"
        )
        assert "<figcaption" not in html

    def test_default_colors(self):
        html = _html(
            "Image {\n"
            "    ImageItem { image: \"./a.jpg\", title: \"T\", description: \"D\" }\n"
            "}\n"
        )
        assert "background-color: #FFFFFF" in html
        assert "border-color: transparent" in html
        assert "color: #000000" in html
        assert "color: #3B3B3B" in html

    def test_item_color_inherited_from_container(self):
        html = _html(
            "Image {\n"
            "    titleColor: \"#112233\"\n"
            "    descriptionColor: \"#445566\"\n"
            "    backgroundColor: \"#EEEEEE\"\n"
            "    borderColor: \"#FF0000\"\n"
            "    ImageItem { image: \"./a.jpg\", title: \"T\", description: \"D\" }\n"
            "}\n"
        )
        assert "color: #112233" in html
        assert "color: #445566" in html
        assert "background-color: #EEEEEE" in html
        assert "border-color: #FF0000" in html

    def test_item_color_overrides_container(self):
        html = _html(
            "Image {\n"
            "    titleColor: \"#112233\"\n"
            "    ImageItem { image: \"./a.jpg\", title: \"T\", titleColor: \"#FF0000\" }\n"
            "}\n"
        )
        assert "color: #FF0000" in html
        assert "color: #112233" not in html

    def test_single_mode_columns_produces_rows(self):
        html = _html(
            "Image {\n"
            "    columns: 2\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "    ImageItem { image: \"./b.jpg\" }\n"
            "    ImageItem { image: \"./c.jpg\" }\n"
            "}\n"
        )
        assert 'class="lk-image-row lk-image-row--plain"' in html
        assert html.count('class="lk-image-row') == 2

    def test_slider_mode(self):
        html = _html(
            "Image {\n"
            "    displayMode: slider\n"
            "    ImageItem { image: \"./a.jpg\", title: \"One\" }\n"
            "    ImageItem { image: \"./b.jpg\" }\n"
            "}\n"
        )
        assert 'class="lk-image lk-image-slider"' in html
        assert 'class="lk-image-slider-track"' in html
        assert "lk-imagecard" in html

    def test_slider_dots_per_slide(self):
        html = _html(
            "Image {\n"
            "    displayMode: slider\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "    ImageItem { image: \"./b.jpg\" }\n"
            "    ImageItem { image: \"./c.jpg\" }\n"
            "}\n"
        )
        assert 'class="lk-image-slider-dots"' in html
        assert html.count('data-slide="') == 3
        assert 'data-slide="0"' in html
        assert 'data-slide="2"' in html
        assert "Go to slide 3" in html

    def test_first_dot_active_then_styles(self):
        html = _html(
            "Image {\n"
            "    displayMode: slider\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "    ImageItem { image: \"./b.jpg\" }\n"
            "}\n"
        )
        assert 'class="lk-image-slider-dot is-active"' in html
        assert 'class="lk-image-slider-dot"' in html
        assert ".lk-image-slider-dot" in html
        assert "border-radius: 50%" in html

    def test_dots_overlay_image_region(self):
        html = _html(
            "Image {\n"
            "    displayMode: slider\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "}\n"
        )
        assert "aspect-ratio: 4 / 3" in html
        assert "pointer-events: none" in html
        assert "pointer-events: auto" in html

    def test_last_slide_fills_viewport(self):
        html = _html(
            "Image {\n"
            "    displayMode: slider\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "    ImageItem { image: \"./b.jpg\" }\n"
            "    ImageItem { image: \"./c.jpg\" }\n"
            "}\n"
        )
        assert "lk-image-slider-track .lk-imagecard:last-child" in html
        assert "flex-basis: 100%" in html

    def test_slider_slides_have_unique_ids(self):
        html = _html(
            "Image {\n"
            "    displayMode: slider\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "    ImageItem { image: \"./b.jpg\" }\n"
            "}\n"
        )
        assert 'id="lk-slider-1"' in html
        assert 'id="lk-slider-1-slide-0"' in html
        assert 'id="lk-slider-1-slide-1"' in html

    def test_slider_js_embedded(self):
        html = _html(
            "Image {\n"
            "    displayMode: slider\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "}\n"
        )
        assert "<script>" in html
        assert "lk-image-slider-dot" in html
        assert "classList.toggle('is-active'" in html
        assert "track.scrollTo" in html

    def test_no_slider_means_no_script(self):
        html = _html(
            "Image {\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "}\n"
        )
        assert "<script>" not in html

    def test_multiple_sliders_unique_ids(self):
        html = _html(
            "Image {\n"
            "    displayMode: slider\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "}\n"
            "Image {\n"
            "    displayMode: slider\n"
            "    ImageItem { image: \"./b.jpg\" }\n"
            "}\n"
        )
        assert 'id="lk-slider-1"' in html
        assert 'id="lk-slider-2"' in html

    def test_image_shadow_class(self):
        html = _html(
            "Image {\n"
            "    imageShadow: true\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "}\n"
        )
        assert "lk-imagecard--shadow" in html

    def test_css_includes_image_styles(self):
        html = _html(self.SRC)
        assert ".lk-image-row" in html
        assert ".lk-imagecard-img" in html
        assert ".lk-image-slider-track" in html
        assert "scroll-snap-type: x mandatory" in html
