"""Tests for semantic validation and default resolution."""

from __future__ import annotations

from tests.helpers import compile_ok

LINK = 'Link { title: "GitHub", url: "https://github.com" }'


class TestRequiredProperties:
    def test_missing_url(self):
        from compiler import SemanticError, compile_source

        errors = compile_source('Link { title: "GitHub" }').errors
        assert len(errors) == 1
        assert isinstance(errors[0], SemanticError)
        assert "required property 'url'" in errors[0].message

    def test_missing_title_reports_title(self):
        from compiler import compile_source

        errors = compile_source('Link { url: "https://github.com" }').errors
        assert len(errors) == 1
        assert "required property 'title'" in errors[0].message


class TestProfileRequiredProperties:
    def _missing(self, source: str, prop: str) -> str:
        from compiler import compile_source

        errors = compile_source(source).errors
        assert len(errors) == 1, errors
        assert "missing the required property" in errors[0].message
        assert f"'{prop}'" in errors[0].message
        return errors[0].message

    def test_name_requires_title(self):
        self._missing("Profile { Name {} }", "title")

    def test_logo_requires_image(self):
        self._missing("Profile { Logo {} }", "image")

    def test_bio_requires_text(self):
        self._missing("Profile { Bio {} }", "text")

    def test_cover_requires_image(self):
        self._missing("Profile { Cover {} }", "image")


class TestPropertyRules:
    def test_unknown_property(self):
        from compiler import compile_source

        errors = compile_source(
            'Link { title: "x", url: "https://x.com", fontSize: 18 }'
        ).errors
        assert len(errors) == 1
        assert "Unknown property 'fontSize'" in errors[0].message

    def test_duplicate_property(self):
        from compiler import compile_source

        errors = compile_source(
            'Link { title: "a", title: "b", url: "https://x.com" }'
        ).errors
        assert len(errors) == 1
        assert "Duplicate property 'title'" in errors[0].message


class TestValueValidation:
    def test_invalid_enum_value(self):
        from compiler import compile_source

        errors = compile_source(
            'Link { title: "x", url: "https://x.com", shape: roundedLarge }'
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message
        assert "sharp, slightlyRounded, rounded, pill" in errors[0].message

    def test_quoted_enum_value(self):
        from compiler import compile_source

        errors = compile_source(
            'Link { title: "x", url: "https://x.com", align: "center" }'
        ).errors
        assert len(errors) == 1
        assert "quotation marks" in errors[0].message

    def test_invalid_url_missing_scheme(self):
        from compiler import compile_source

        errors = compile_source('Link { title: "x", url: "github.com" }').errors
        assert len(errors) == 1
        assert "URL" in errors[0].message

    def test_invalid_url_unsupported_scheme(self):
        from compiler import compile_source

        errors = compile_source(
            'Link { title: "x", url: "ftp://github.com" }'
        ).errors
        assert len(errors) == 1
        assert "URL" in errors[0].message

    def test_invalid_color(self):
        from compiler import compile_source

        errors = compile_source(
            'Link { title: "x", url: "https://x.com", backgroundColor: "red" }'
        ).errors
        assert len(errors) == 1
        assert "Color" in errors[0].message

    def test_invalid_type_boolean_for_string(self):
        from compiler import compile_source

        errors = compile_source(
            'Link { title: true, url: "https://x.com" }'
        ).errors
        assert len(errors) == 1
        assert "String" in errors[0].message

    def test_valid_transparent_border(self):
        compile_ok('Link { title: "x", url: "https://x.com", borderColor: transparent }')

    def test_valid_hex_color_short(self):
        compile_ok('Link { title: "x", url: "https://x.com", titleColor: "#FFF" }')

    def test_all_optional_properties(self):
        compile_ok(
            'Link {\n'
            '        title: "Portfolio"\n'
            '        url: "https://example.com"\n'
            '        align: left\n'
            '        titleColor: "#FFFFFF"\n'
            '        backgroundColor: "#3B82F6"\n'
            '        borderColor: "#2563EB"\n'
            '        shape: pill\n'
            '    }'
        )


class TestBlockRules:
    def test_unknown_block(self):
        from compiler import SemanticError, compile_source

        errors = compile_source('MagicButton {}').errors
        assert len(errors) == 1
        assert isinstance(errors[0], SemanticError)
        assert "Unknown block 'MagicButton'" in errors[0].message

    def test_repeatable_links_allowed(self):
        compile_ok(f"{LINK}\n{LINK}")


class TestTitle:
    def _first_title(self, source: str):
        result = compile_ok(source)
        assert result.ast is not None
        return result.ast.blocks[0]

    def test_missing_title(self):
        from compiler import SemanticError, compile_source

        errors = compile_source("Title {}").errors
        assert len(errors) == 1
        assert isinstance(errors[0], SemanticError)
        assert "required property 'title'" in errors[0].message

    def test_invalid_text_align(self):
        from compiler import compile_source

        errors = compile_source(
            'Title { title: "x", align: justify }'
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message
        assert "left, center, right" in errors[0].message

    def test_defaults_applied(self):
        block = self._first_title('Title { title: "My Links" }')
        assert block.resolved == {
            "title": "My Links",
            "align": "center",
            "titleColor": "#000000",
        }

    def test_explicit_values_override_defaults(self):
        block = self._first_title(
            'Title { title: "x", align: left, titleColor: "#c7006e" }'
        )
        assert block.resolved["align"] == "left"
        assert block.resolved["titleColor"] == "#c7006e"

    def test_repeatable_titles_allowed(self):
        compile_ok('Title { title: "A" }\nTitle { title: "B" }')

    def test_title_outside_profile_allowed(self):
        compile_ok('Title { title: "My Links" }')


class TestText:
    def _first_text(self, source: str):
        result = compile_ok(source)
        assert result.ast is not None
        return result.ast.blocks[0]

    def test_missing_text(self):
        from compiler import SemanticError, compile_source

        errors = compile_source("Text {}").errors
        assert len(errors) == 1
        assert isinstance(errors[0], SemanticError)
        assert "required property 'text'" in errors[0].message

    def test_invalid_shape_value(self):
        from compiler import compile_source

        errors = compile_source('Text { text: "x", shape: squircle }').errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message
        assert "sharp, slightlyRounded, rounded, pill" in errors[0].message

    def test_defaults_applied(self):
        block = self._first_text('Text { text: "Hello" }')
        assert block.resolved == {
            "text": "Hello",
            "align": "center",
            "textColor": "#000000",
            "backgroundColor": "transparent",
            "borderColor": "transparent",
            "shape": "rounded",
        }

    def test_explicit_values_override_defaults(self):
        block = self._first_text(
            'Text { text: "x", align: left, textColor: "#333333", shape: pill }'
        )
        assert block.resolved["align"] == "left"
        assert block.resolved["textColor"] == "#333333"
        assert block.resolved["shape"] == "pill"

    def test_repeatable_texts_allowed(self):
        compile_ok('Text { text: "A" }\nText { text: "B" }')


class TestSocialMedia:
    SRC = (
        "SocialMedia {\n"
        "    SocialMediaItem { service: instagram, url: \"https://ig/x\" }\n"
        "}\n"
    )

    def test_valid_socialmedia(self):
        compile_ok(self.SRC)

    def test_item_requires_url(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialMedia {\n"
            "    SocialMediaItem { service: instagram }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'url'" in errors[0].message

    def test_item_requires_service(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialMedia {\n"
            "    SocialMediaItem { url: \"https://ig/x\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'service'" in errors[0].message

    def test_invalid_service(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialMedia {\n"
            "    SocialMediaItem { service: myspace, url: \"https://x.com\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message

    def test_invalid_columns_value(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialMedia {\n"
            "    columns: 5\n"
            "    SocialMediaItem { service: instagram, url: \"https://ig/x\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'columns' must be one of 1, 2, 3, 4" in errors[0].message

    def test_columns_default_is_one(self):
        result = compile_ok("SocialMedia {\n"
            "    SocialMediaItem { service: instagram, url: \"https://ig/x\" }\n"
            "}\n")
        assert result.ast is not None
        assert result.ast.blocks[0].resolved["columns"] == 1

    def test_columns_four_rejected_when_icon_and_title_shown(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialMedia {\n"
            "    columns: 4\n"
            "    SocialMediaItem { service: instagram, url: \"https://ig/x\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'columns' can only be 4" in errors[0].message

    def test_columns_four_allowed_when_title_hidden(self):
        compile_ok("SocialMedia {\n"
            "    columns: 4\n"
            "    showTitle: false\n"
            "    SocialMediaItem { service: instagram, url: \"https://ig/x\" }\n"
            "}\n")

    def test_columns_four_allowed_when_icon_hidden(self):
        compile_ok("SocialMedia {\n"
            "    columns: 4\n"
            "    showIcon: false\n"
            "    SocialMediaItem { service: instagram, url: \"https://ig/x\" }\n"
            "}\n")

    def test_show_both_false_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialMedia {\n"
            "    showTitle: false\n"
            "    showIcon: false\n"
            "    SocialMediaItem { service: instagram, url: \"https://ig/x\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'showTitle' and 'showIcon' cannot both be false" in errors[0].message

    def test_empty_socialmedia_rejected(self):
        from compiler import compile_source

        errors = compile_source("SocialMedia {\n}\n").errors
        assert len(errors) == 1
        assert "at least one 'SocialMediaItem'" in errors[0].message

    def test_item_outside_socialmedia_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialMediaItem { service: instagram, url: \"https://ig/x\" }\n"
        ).errors
        assert len(errors) == 1
        assert "only allowed inside" in errors[0].message


class TestSocialNetwork:
    SRC = (
        "SocialNetwork {\n"
        "    SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
        "}\n"
    )

    def test_valid_socialnetwork(self):
        compile_ok(self.SRC)

    def test_item_requires_url(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialNetwork {\n"
            "    SocialNetworkItem { service: whatsapp }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'url'" in errors[0].message

    def test_item_requires_service(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialNetwork {\n"
            "    SocialNetworkItem { url: \"https://wa.me/1\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'service'" in errors[0].message

    def test_invalid_service(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialNetwork {\n"
            "    SocialNetworkItem { service: myspace, url: \"https://x.com\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message

    def test_invalid_columns_value(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialNetwork {\n"
            "    columns: 5\n"
            "    SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'columns' must be one of 1, 2, 3, 4" in errors[0].message

    def test_columns_default_is_one(self):
        result = compile_ok("SocialNetwork {\n"
            "    SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
            "}\n")
        assert result.ast is not None
        assert result.ast.blocks[0].resolved["columns"] == 1

    def test_columns_four_rejected_when_icon_and_title_shown(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialNetwork {\n"
            "    columns: 4\n"
            "    SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'columns' can only be 4" in errors[0].message

    def test_columns_four_allowed_when_title_hidden(self):
        compile_ok("SocialNetwork {\n"
            "    columns: 4\n"
            "    showTitle: false\n"
            "    SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
            "}\n")

    def test_columns_four_allowed_when_icon_hidden(self):
        compile_ok("SocialNetwork {\n"
            "    columns: 4\n"
            "    showIcon: false\n"
            "    SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
            "}\n")

    def test_show_both_false_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialNetwork {\n"
            "    showTitle: false\n"
            "    showIcon: false\n"
            "    SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'showTitle' and 'showIcon' cannot both be false" in errors[0].message

    def test_empty_socialnetwork_rejected(self):
        from compiler import compile_source

        errors = compile_source("SocialNetwork {\n}\n").errors
        assert len(errors) == 1
        assert "at least one 'SocialNetworkItem'" in errors[0].message

    def test_item_outside_socialnetwork_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
        ).errors
        assert len(errors) == 1
        assert "only allowed inside" in errors[0].message

    def test_valid_network_services(self):
        compile_ok("SocialNetwork {\n"
            "    SocialNetworkItem { service: telegram, url: \"https://t.me/x\" }\n"
            "    SocialNetworkItem { service: whatsapp, url: \"https://wa.me/1\" }\n"
            "    SocialNetworkItem { service: discord, url: \"https://d.gg/x\" }\n"
            "    SocialNetworkItem { service: skype, url: \"https://skype.com\" }\n"
            "    SocialNetworkItem { service: line, url: \"https://line.me\" }\n"
            "    SocialNetworkItem { service: viber, url: \"https://viber.com\" }\n"
            "    SocialNetworkItem { service: kik, url: \"https://kik.com\" }\n"
            "    SocialNetworkItem { service: facebookMessenger, url: \"https://m.me/x\" }\n"
            "    SocialNetworkItem { service: bale, url: \"https://ble.ir/x\" }\n"
            "    SocialNetworkItem { service: eitaa, url: \"https://eitaa.com/x\" }\n"
            "    SocialNetworkItem { service: rubika, url: \"https://rubika.ir/x\" }\n"
            "}\n")

    def test_socialmedia_service_rejected_in_socialnetwork(self):
        from compiler import compile_source

        errors = compile_source(
            "SocialNetwork {\n"
            "    SocialNetworkItem { service: instagram, url: \"https://ig/x\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message


class TestProfileRules:
    def test_profile_not_repeatable(self):
        from compiler import compile_source

        errors = compile_source('Profile {}\nProfile {}').errors
        assert len(errors) >= 1
        assert "may appear only once" in errors[0].message

    def test_name_outside_profile_rejected(self):
        from compiler import SemanticError, compile_source

        errors = compile_source('Name { title: "Test" }').errors
        assert len(errors) == 1
        assert isinstance(errors[0], SemanticError)
        assert "only allowed inside" in errors[0].message

    def test_logo_outside_profile_rejected(self):
        from compiler import SemanticError, compile_source

        errors = compile_source('Logo { image: "https://x.com/a.jpg" }').errors
        assert len(errors) == 1
        assert "only allowed inside" in errors[0].message

    def test_bio_outside_profile_rejected(self):
        from compiler import SemanticError, compile_source

        errors = compile_source('Bio { text: "Hello" }').errors
        assert len(errors) == 1
        assert "only allowed inside" in errors[0].message

    def test_cover_outside_profile_rejected(self):
        from compiler import SemanticError, compile_source

        errors = compile_source('Cover { image: "https://x.com/a.jpg" }').errors
        assert len(errors) == 1
        assert len(errors) == 1
        assert "only allowed inside" in errors[0].message

    def test_invalid_image_extension(self):
        from compiler import compile_source

        errors = compile_source(
            'Profile { Logo { image: "https://x.com/file.txt" } }'
        ).errors
        assert len(errors) == 1
        assert "image URL" in errors[0].message

    def test_valid_image_url(self):
        compile_ok('Profile { Logo { image: "https://x.com/photo.jpg" } }')

    def test_valid_image_local_path(self):
        compile_ok('Profile { Logo { image: "./assets/photo.png" } }')


class TestDefaultResolution:
    def _first_link(self, source: str):
        result = compile_ok(source)
        assert result.ast is not None
        return result.ast.blocks[0]

    def test_defaults_applied(self):
        block = self._first_link(LINK)
        assert block.resolved == {
            "title": "GitHub",
            "url": "https://github.com",
            "align": "center",
            "titleColor": "#FFFFFF",
            "backgroundColor": "#00B4B0",
            "borderColor": "transparent",
            "shape": "rounded",
        }

    def test_explicit_values_override_defaults(self):
        block = self._first_link(
            'Link { title: "x", url: "https://x.com", '
            'align: right, shape: pill, backgroundColor: "#000000" }'
        )
        assert block.resolved["align"] == "right"
        assert block.resolved["shape"] == "pill"
        assert block.resolved["backgroundColor"] == "#000000"
        assert block.resolved["titleColor"] == "#FFFFFF"

    def test_escape_sequences_decoded(self):
        block = self._first_link(
            'Link { title: "He said \\"Hi\\"\\nNext", url: "https://x.com" }'
        )
        assert block.resolved["title"] == 'He said "Hi"\nNext'


class TestContact:
    SRC = (
        "Contact {\n"
        "    ContactItem { service: email, value: \"hi@example.com\" }\n"
        "}\n"
    )

    def test_valid_contact(self):
        compile_ok(self.SRC)

    def test_item_requires_value(self):
        from compiler import compile_source

        errors = compile_source(
            "Contact {\n"
            "    ContactItem { service: email }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'value'" in errors[0].message

    def test_valid_all_types(self):
        compile_ok("Contact {\n"
            "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
            "    ContactItem { service: phone, value: \"+1 234 567 8901\" }\n"
            "    ContactItem { service: email, value: \"hi@example.com\" }\n"
            "    ContactItem { service: sms, value: \"+1 234 567 8901\" }\n"
            "    ContactItem { service: website, value: \"https://example.com\" }\n"
            "}\n")

    def test_invalid_type(self):
        from compiler import compile_source

        errors = compile_source(
            "Contact {\n"
            "    ContactItem { service: fax, value: \"+1 234 567 8901\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message

    def test_invalid_columns_value(self):
        from compiler import compile_source

        errors = compile_source(
            "Contact {\n"
            "    columns: 5\n"
            "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'columns' must be one of 1, 2, 3, 4" in errors[0].message

    def test_columns_default_is_one(self):
        result = compile_ok("Contact {\n"
            "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
            "}\n")
        assert result.ast is not None
        assert result.ast.blocks[0].resolved["columns"] == 1

    def test_columns_four_rejected_when_icon_and_title_shown(self):
        from compiler import compile_source

        errors = compile_source(
            "Contact {\n"
            "    columns: 4\n"
            "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'columns' can only be 4" in errors[0].message

    def test_columns_four_allowed_when_title_hidden(self):
        compile_ok("Contact {\n"
            "    columns: 4\n"
            "    showTitle: false\n"
            "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
            "}\n")

    def test_columns_four_allowed_when_icon_hidden(self):
        compile_ok("Contact {\n"
            "    columns: 4\n"
            "    showIcon: false\n"
            "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
            "}\n")

    def test_show_both_false_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            "Contact {\n"
            "    showTitle: false\n"
            "    showIcon: false\n"
            "    ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'showTitle' and 'showIcon' cannot both be false" in errors[0].message

    def test_empty_contact_rejected(self):
        from compiler import compile_source

        errors = compile_source("Contact {\n}\n").errors
        assert len(errors) == 1
        assert "at least one 'ContactItem'" in errors[0].message

    def test_item_outside_contact_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            "ContactItem { service: mobile, value: \"+1 234 567 8901\" }\n"
        ).errors
        assert len(errors) == 1
        assert "only allowed inside" in errors[0].message

    def test_item_requires_service(self):
        from compiler import compile_source

        errors = compile_source(
            "Contact {\n"
            "    ContactItem { value: \"+1 234 567 8901\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'service'" in errors[0].message


class TestAddress:
    SRC = (
        "Address {\n"
        "    AddressItem { service: googleMap, url: \"https://maps.google.com/?q=T\" }\n"
        "}\n"
    )

    def test_valid_address(self):
        compile_ok(self.SRC)

    def test_item_requires_url(self):
        from compiler import compile_source

        errors = compile_source(
            "Address {\n"
            "    AddressItem { service: googleMap }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'url'" in errors[0].message

    def test_valid_all_services(self):
        compile_ok("Address {\n"
            "    AddressItem { service: googleMap, url: \"https://g/x\" }\n"
            "    AddressItem { service: waze, url: \"https://w/x\" }\n"
            "    AddressItem { service: neshan, url: \"https://n/x\" }\n"
            "    AddressItem { service: balad, url: \"https://b/x\" }\n"
            "}\n")

    def test_invalid_service(self):
        from compiler import compile_source

        errors = compile_source(
            "Address {\n"
            "    AddressItem { service: mapQuest, url: \"https://x.com\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message

    def test_address_and_color_accepted(self):
        compile_ok("Address {\n"
            "    address: \"Tehran, Iran\"\n"
            "    addressColor: \"#111111\"\n"
            "    AddressItem { service: waze, url: \"https://w/x\" }\n"
            "}\n")

    def test_address_color_default_is_black(self):
        result = compile_ok(self.SRC)
        assert result.ast is not None
        assert result.ast.blocks[0].resolved["addressColor"] == "#000000"

    def test_invalid_columns_value(self):
        from compiler import compile_source

        errors = compile_source(
            "Address {\n"
            "    columns: 5\n"
            "    AddressItem { service: googleMap, url: \"https://g/x\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'columns' must be one of 1, 2, 3, 4" in errors[0].message

    def test_columns_default_is_one(self):
        result = compile_ok(self.SRC)
        assert result.ast is not None
        assert result.ast.blocks[0].resolved["columns"] == 1

    def test_columns_four_rejected_when_icon_and_title_shown(self):
        from compiler import compile_source

        errors = compile_source(
            "Address {\n"
            "    columns: 4\n"
            "    AddressItem { service: googleMap, url: \"https://g/x\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'columns' can only be 4" in errors[0].message

    def test_columns_four_allowed_when_title_hidden(self):
        compile_ok("Address {\n"
            "    columns: 4\n"
            "    showTitle: false\n"
            "    AddressItem { service: googleMap, url: \"https://g/x\" }\n"
            "}\n")

    def test_show_both_false_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            "Address {\n"
            "    showTitle: false\n"
            "    showIcon: false\n"
            "    AddressItem { service: googleMap, url: \"https://g/x\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "'showTitle' and 'showIcon' cannot both be false" in errors[0].message

    def test_empty_address_rejected(self):
        from compiler import compile_source

        errors = compile_source("Address {\n}\n").errors
        assert len(errors) == 1
        assert "at least one 'AddressItem'" in errors[0].message

    def test_item_outside_address_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            "AddressItem { service: googleMap, url: \"https://g/x\" }\n"
        ).errors
        assert len(errors) == 1
        assert "only allowed inside" in errors[0].message

    def test_item_requires_service(self):
        from compiler import compile_source

        errors = compile_source(
            "Address {\n"
            "    AddressItem { url: \"https://g/x\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'service'" in errors[0].message


class TestImage:
    SRC = (
        "Image {\n"
        "    ImageItem { image: \"./assets/one.jpg\" }\n"
        "}\n"
    )

    def test_valid_image(self):
        compile_ok(self.SRC)

    def test_item_requires_image(self):
        from compiler import compile_source

        errors = compile_source(
            "Image {\n"
            "    ImageItem { }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'image'" in errors[0].message

    def test_requires_at_least_one_child(self):
        from compiler import compile_source

        errors = compile_source("Image { }\n").errors
        assert len(errors) == 1
        assert "at least one 'ImageItem'" in errors[0].message

    def test_defaults(self):
        result = compile_ok(self.SRC)
        assert result.ast is not None
        block = result.ast.blocks[0]
        assert block.resolved["displayMode"] == "single"
        assert block.resolved["columns"] == 1
        assert block.resolved["titleColor"] == "#000000"
        assert block.resolved["descriptionColor"] == "#3B3B3B"
        assert block.resolved["backgroundColor"] == "#FFFFFF"
        assert block.resolved["borderColor"] == "transparent"
        assert block.resolved["shape"] == "rounded"
        assert block.resolved["imageShadow"] is False

    def test_item_color_defaults_inherit(self):
        result = compile_ok(self.SRC)
        assert result.ast is not None
        item = result.ast.blocks[0].children[0]
        assert item.resolved["titleColor"] == ""
        assert item.resolved["descriptionColor"] == ""
        assert item.resolved["backgroundColor"] == ""
        assert item.resolved["borderColor"] == ""

    def test_single_mode_valid_columns_one_and_two(self):
        compile_ok("Image {\n"
            "    columns: 1\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "    ImageItem { image: \"./b.jpg\" }\n"
            "}\n")
        compile_ok("Image {\n"
            "    columns: 2\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "    ImageItem { image: \"./b.jpg\" }\n"
            "}\n")

    def test_single_mode_invalid_columns_three_or_more(self):
        from compiler import compile_source

        for columns in (3, 4, 5):
            errors = compile_source(
                f"Image {{\n"
                f"    columns: {columns}\n"
                f"    ImageItem {{ image: \"./a.jpg\" }}\n"
                f"}}\n"
            ).errors
            assert len(errors) == 1
            assert "columns" in errors[0].message

    def test_columns_ignored_in_slider_mode(self):
        compile_ok("Image {\n"
            "    displayMode: slider\n"
            "    columns: 4\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "}\n")

    def test_invalid_display_mode(self):
        from compiler import compile_source

        errors = compile_source(
            "Image {\n"
            "    displayMode: carousel\n"
            "    ImageItem { image: \"./a.jpg\" }\n"
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message

    def test_imageitem_only_allowed_inside_image(self):
        from compiler import compile_source

        errors = compile_source("ImageItem { image: \"./a.jpg\" }\n").errors
        assert len(errors) == 1
        assert "only allowed inside" in errors[0].message


class TestBanner:
    SRC = (
        "Banner {\n"
        '    BannerItem { image: "./a.jpg", url: "https://example.com" }\n'
        "}\n"
    )

    def test_valid_banner(self):
        compile_ok(self.SRC)

    def test_item_requires_image(self):
        from compiler import compile_source

        errors = compile_source(
            "Banner {\n"
            '    BannerItem { url: "https://example.com" }\n'
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'image'" in errors[0].message

    def test_item_requires_url(self):
        from compiler import compile_source

        errors = compile_source(
            "Banner {\n"
            '    BannerItem { image: "./a.jpg" }\n'
            "}\n"
        ).errors
        assert len(errors) == 1
        assert "required property 'url'" in errors[0].message

    def test_requires_at_least_one_child(self):
        from compiler import compile_source

        errors = compile_source("Banner { }\n").errors
        assert len(errors) == 1
        assert "at least one 'BannerItem'" in errors[0].message

    def test_defaults(self):
        result = compile_ok(self.SRC)
        assert result.ast is not None
        block = result.ast.blocks[0]
        assert block.resolved["columns"] == 1
        assert block.resolved["titleColor"] == "#FFFFFF"
        assert block.resolved["descriptionColor"] == "#FFFFFF"
        assert block.resolved["borderColor"] == "transparent"
        assert block.resolved["shape"] == "rounded"

    def test_item_color_defaults_inherit(self):
        result = compile_ok(self.SRC)
        assert result.ast is not None
        item = result.ast.blocks[0].children[0]
        assert item.resolved["titleColor"] == ""
        assert item.resolved["descriptionColor"] == ""
        assert item.resolved["borderColor"] == ""

    def test_valid_columns_one_and_two(self):
        compile_ok("Banner {\n"
            "    columns: 1\n"
            '    BannerItem { image: "./a.jpg", url: "https://example.com" }\n'
            "}\n")
        compile_ok("Banner {\n"
            "    columns: 2\n"
            '    BannerItem { image: "./a.jpg", url: "https://example.com" }\n'
            "}\n")

    def test_invalid_columns_three_or_more(self):
        from compiler import compile_source

        for columns in (3, 4, 5):
            errors = compile_source(
                f"Banner {{\n"
                f"    columns: {columns}\n"
                f'    BannerItem {{ image: "./a.jpg", url: "https://example.com" }}\n'
                f"}}\n"
            ).errors
            assert len(errors) == 1
            assert "columns" in errors[0].message

    def test_banneritem_only_allowed_inside_banner(self):
        from compiler import compile_source

        errors = compile_source(
            'BannerItem { image: "./a.jpg", url: "https://example.com" }\n'
        ).errors
        assert len(errors) == 1
        assert "only allowed inside" in errors[0].message


class TestVideo:
    def test_valid_youtube(self):
        compile_ok('Video { url: "https://www.youtube.com/watch?v=abc123" }\n')

    def test_valid_youtube_short(self):
        compile_ok('Video { url: "https://youtu.be/abc123" }\n')

    def test_valid_aparat(self):
        compile_ok('Video { url: "https://www.aparat.com/v/abc123" }\n')

    def test_valid_local_mp4(self):
        compile_ok('Video { url: "./assets/intro.mp4" }\n')

    def test_valid_local_webm(self):
        compile_ok('Video { url: "./assets/intro.webm" }\n')

    def test_valid_local_mov(self):
        compile_ok('Video { url: "./assets/intro.mov" }\n')

    def test_requires_url(self):
        from compiler import compile_source

        errors = compile_source("Video { }\n").errors
        assert len(errors) == 1
        assert "required property 'url'" in errors[0].message

    def test_invalid_url(self):
        from compiler import compile_source

        errors = compile_source('Video { url: "not-a-url" }\n').errors
        assert len(errors) == 1
        assert "expected a YouTube URL" in errors[0].message

    def test_defaults(self):
        result = compile_ok('Video { url: "https://www.youtube.com/watch?v=abc123" }\n')
        assert result.ast is not None
        block = result.ast.blocks[0]
        assert block.resolved["thumbnail"] == ""
        assert block.resolved["shape"] == "rounded"
        assert block.resolved["borderColor"] == "transparent"

    def test_repeatable(self):
        compile_ok(
            'Video { url: "https://www.youtube.com/watch?v=abc123" }\n'
            'Video { url: "https://www.youtube.com/watch?v=def456" }\n'
        )

    def test_custom_thumbnail(self):
        compile_ok(
            'Video { url: "https://www.youtube.com/watch?v=abc123", thumbnail: "./thumb.jpg" }\n'
        )

    def test_custom_shape(self):
        compile_ok(
            'Video { url: "https://www.youtube.com/watch?v=abc123", shape: pill }\n'
        )

    def test_invalid_shape(self):
        from compiler import compile_source

        errors = compile_source(
            'Video { url: "https://www.youtube.com/watch?v=abc123", shape: circle }\n'
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message

    def test_invalid_border_color(self):
        from compiler import compile_source

        errors = compile_source(
            'Video { url: "https://www.youtube.com/watch?v=abc123", borderColor: "red" }\n'
        ).errors
        assert len(errors) == 1
        assert "valid Color" in errors[0].message


class TestCountdown:
    SRC = 'Countdown { date: "2026/12/31", time: "23:59", calendar: gregorian }\n'

    def test_valid(self):
        compile_ok(self.SRC)

    def test_requires_date(self):
        from compiler import compile_source

        errors = compile_source('Countdown { time: "23:59" }\n').errors
        assert len(errors) == 1
        assert "required property 'date'" in errors[0].message

    def test_requires_time(self):
        from compiler import compile_source

        errors = compile_source('Countdown { date: "1404/09/15" }\n').errors
        assert len(errors) == 1
        assert "required property 'time'" in errors[0].message

    def test_empty_block_requires_both(self):
        from compiler import compile_source

        errors = compile_source("Countdown { }\n").errors
        assert len(errors) == 2
        messages = [e.message for e in errors]
        assert any("required property 'date'" in m for m in messages)
        assert any("required property 'time'" in m for m in messages)

    def test_invalid_date_format(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "hello", time: "23:59", calendar: gregorian }\n'
        ).errors
        assert len(errors) == 1
        assert "valid date" in errors[0].message

    def test_invalid_date_no_slashes(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "31122026", time: "23:59", calendar: gregorian }\n'
        ).errors
        assert len(errors) == 1
        assert "valid date" in errors[0].message

    def test_invalid_date_impossible(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "2026/13/40", time: "23:59", calendar: gregorian }\n'
        ).errors
        assert len(errors) == 1
        assert "valid date" in errors[0].message

    def test_invalid_date_leap_year(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "2025/02/29", time: "00:00", calendar: gregorian }\n'
        ).errors
        assert len(errors) == 1
        assert "valid date" in errors[0].message

    def test_valid_leap_year(self):
        compile_ok('Countdown { date: "2024/02/29", time: "00:00", calendar: gregorian }\n')

    def test_invalid_time_format(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "2026/12/31", time: "noon", calendar: gregorian }\n'
        ).errors
        assert len(errors) == 1
        assert "valid time" in errors[0].message

    def test_invalid_time_out_of_range(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "2026/12/31", time: "25:00", calendar: gregorian }\n'
        ).errors
        assert len(errors) == 1
        assert "valid time" in errors[0].message

    def test_invalid_minute_out_of_range(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "2026/12/31", time: "12:61", calendar: gregorian }\n'
        ).errors
        assert len(errors) == 1
        assert "valid time" in errors[0].message

    def test_defaults(self):
        result = compile_ok('Countdown { date: "1404/09/15", time: "23:59" }\n')
        block = result.ast.blocks[0]
        assert block.resolved["expiredText"] == ""
        assert block.resolved["language"] == "fa"
        assert block.resolved["calendar"] == "jalali"
        assert block.resolved["textColor"] == "#00B4B0"
        assert block.resolved["backgroundColor"] == "transparent"
        assert block.resolved["borderColor"] == "transparent"
        assert block.resolved["shape"] == "rounded"

    def test_calendar_valid_gregorian(self):
        compile_ok('Countdown { date: "2026/12/31", time: "23:59", calendar: gregorian }\n')

    def test_calendar_valid_jalali(self):
        compile_ok('Countdown { date: "1404/09/15", time: "23:59", calendar: jalali }\n')

    def test_calendar_invalid(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "2026/12/31", time: "23:59", calendar: lunar }\n'
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message

    def test_calendar_quoted_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "2026/12/31", time: "23:59", calendar: "jalali" }\n'
        ).errors
        assert len(errors) == 1
        assert "quotation marks" in errors[0].message

    def test_jalali_date_accepted_with_jalali_calendar(self):
        compile_ok('Countdown { date: "1404/09/15", time: "12:00", calendar: jalali }\n')

    def test_jalali_leap_day_accepted(self):
        compile_ok('Countdown { date: "1399/12/30", time: "00:00", calendar: jalali }\n')

    def test_gregorian_date_rejected_under_jalali_calendar(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "2026/13/40", time: "23:59", calendar: jalali }\n'
        ).errors
        assert len(errors) == 1
        assert "Jalali" in errors[0].message

    def test_jalali_impossible_day_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "1404/07/31", time: "23:59", calendar: jalali }\n'
        ).errors
        assert len(errors) == 1
        assert "Jalali" in errors[0].message

    def test_jalali_non_leap_esfand_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "1400/12/30", time: "00:00", calendar: jalali }\n'
        ).errors
        assert len(errors) == 1
        assert "Jalali" in errors[0].message

    def test_language_valid_fa(self):
        compile_ok('Countdown { date: "1404/09/15", time: "23:59", language: fa }\n')

    def test_language_valid_en(self):
        compile_ok('Countdown { date: "1404/09/15", time: "23:59", language: en }\n')

    def test_language_invalid(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "1404/09/15", time: "23:59", language: de }\n'
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message

    def test_language_quoted_rejected(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "1404/09/15", time: "23:59", language: "fa" }\n'
        ).errors
        assert len(errors) == 1
        assert "quotation marks" in errors[0].message

    def test_repeatable(self):
        compile_ok(
            'Countdown { date: "2026/12/31", time: "23:59", calendar: gregorian }\n'
            'Countdown { date: "2026/01/01", time: "00:00", calendar: gregorian }\n'
        )

    def test_invalid_shape(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "2026/12/31", time: "23:59", shape: circle, calendar: gregorian }\n'
        ).errors
        assert len(errors) == 1
        assert "not a valid value" in errors[0].message

    def test_invalid_text_color(self):
        from compiler import compile_source

        errors = compile_source(
            'Countdown { date: "2026/12/31", time: "23:59", textColor: "red", calendar: gregorian }\n'
        ).errors
        assert len(errors) == 1
        assert "valid Color" in errors[0].message

    def test_all_explicit_values(self):
        compile_ok(
            'Countdown {\n'
            '  date: "2026/07/04"\n'
            '  time: "14:00"\n'
            '  expiredText: "Started!"\n'
            '  language: en\n'
            '  textColor: "#FFFFFF"\n'
            '  backgroundColor: "#000000"\n'
            '  borderColor: "#111111"\n'
            '  shape: sharp\n'
            '}\n'
        )


class TestFAQ:
    SRC = (
        "FAQ {\n"
        '    FAQItem { question: "Q1", answer: "A1" }\n'
        '    FAQItem { question: "Q2", answer: "A2" }\n'
        "}\n"
    )

    def test_valid_faq(self):
        compile_ok(self.SRC)

    def test_item_requires_question(self):
        from compiler import compile_source

        errors = compile_source('FAQ { FAQItem { answer: "A" } }\n').errors
        assert len(errors) == 1
        assert "required property 'question'" in errors[0].message

    def test_item_requires_answer(self):
        from compiler import compile_source

        errors = compile_source('FAQ { FAQItem { question: "Q" } }\n').errors
        assert len(errors) == 1
        assert "required property 'answer'" in errors[0].message

    def test_requires_at_least_one_child(self):
        from compiler import compile_source

        errors = compile_source("FAQ { }\n").errors
        assert len(errors) == 1
        assert "at least one 'FAQItem'" in errors[0].message

    def test_defaults(self):
        result = compile_ok(self.SRC)
        assert result.ast is not None
        block = result.ast.blocks[0]
        assert block.resolved["questionColor"] == "#00B4B0"
        assert block.resolved["answerColor"] == "#3B3B3B"
        assert block.resolved["iconColor"] == "#00B4B0"
        assert block.resolved["backgroundColor"] == "#FFFFFF"
        assert block.resolved["borderColor"] == "#00B4B0"
        assert block.resolved["shape"] == "rounded"

    def test_item_color_defaults_inherit(self):
        result = compile_ok(self.SRC)
        assert result.ast is not None
        item = result.ast.blocks[0].children[0]
        assert item.resolved["questionColor"] == ""
        assert item.resolved["answerColor"] == ""
        assert item.resolved["iconColor"] == ""
        assert item.resolved["backgroundColor"] == ""
        assert item.resolved["borderColor"] == ""

    def test_repeatable(self):
        compile_ok(
            "FAQ {\n"
            '    FAQItem { question: "Q1", answer: "A1" }\n'
            "}\n"
            "FAQ {\n"
            '    FAQItem { question: "Q2", answer: "A2" }\n'
            "}\n"
        )

    def test_item_color_override(self):
        compile_ok(
            "FAQ {\n"
            '    FAQItem { question: "Q", answer: "A", questionColor: "#FF0000", iconColor: "#00FF00", backgroundColor: "#000000", borderColor: "#111111" }\n'
            "}\n"
        )

    def test_faqitem_only_allowed_inside_faq(self):
        from compiler import compile_source

        errors = compile_source('FAQItem { question: "Q", answer: "A" }\n').errors
        assert len(errors) == 1
        assert "only allowed inside" in errors[0].message

    def test_unknown_shape_property(self):
        from compiler import compile_source

        errors = compile_source(
            'FAQ { FAQItem { question: "Q", answer: "A", shape: pill } }\n'
        ).errors
        assert len(errors) == 1
        assert "Unknown property 'shape'" in errors[0].message
