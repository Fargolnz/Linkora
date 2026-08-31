"""Declarative definition of the Linkora language.

Every block and every property accepted by the language is described here as
plain data. Adding a new block to the language is a matter of:

1. Adding a ``PropertyDef`` tuple for its properties, and
2. Registering a ``BlockDef`` in the :data:`BLOCKS` table.
3. Adding a renderer for it in :mod:`compiler.codegen`.

Semantic validation and code generation are driven entirely by this data, so
no other compiler code needs to change.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ValueType(Enum):
    """The set of property value types supported by the language."""

    STRING = "String"
    NUMBER = "Number"
    BOOLEAN = "Boolean"
    COLOR = "Color"
    URL = "URL"
    FILE = "File"
    IMAGE = "Image"
    ENUM = "Enum"


@dataclass(frozen=True)
class PropertyDef:
    """The definition of a single block property."""

    name: str
    type: ValueType
    default: object
    required: bool = False
    enum_values: tuple[str, ...] = ()


@dataclass(frozen=True)
class BlockDef:
    """The definition of a single block."""

    name: str
    #: Name of the only parent block that may contain this block, or ``None``
    #: for the root ``Page`` block.
    parent: Optional[str]
    repeatable: bool = False
    allowed_children: tuple[str, ...] = ()
    properties: dict[str, "PropertyDef"] = field(default_factory=dict)

    def property(self, name: str) -> Optional[PropertyDef]:
        return self.properties.get(name)


def _properties(*defs: PropertyDef) -> dict[str, PropertyDef]:
    return {prop.name: prop for prop in defs}


# ---------------------------------------------------------------------------
# Block definitions
# ---------------------------------------------------------------------------

_LINK = BlockDef(
    name="Link",
    parent=None,
    repeatable=True,
    properties=_properties(
        PropertyDef("title", ValueType.STRING, "", required=True),
        PropertyDef("url", ValueType.URL, "", required=True),
        PropertyDef(
            "align",
            ValueType.ENUM,
            "center",
            enum_values=("left", "center", "right"),
        ),
        PropertyDef("titleColor", ValueType.COLOR, "#FFFFFF"),
        PropertyDef("backgroundColor", ValueType.COLOR, "#00B4B0"),
        PropertyDef("borderColor", ValueType.COLOR, "transparent"),
        PropertyDef(
            "shape",
            ValueType.ENUM,
            "rounded",
            enum_values=("sharp", "slightlyRounded", "rounded", "pill"),
        ),
    ),
)

_PROFILE = BlockDef(
    name="Profile",
    parent=None,
    repeatable=False,
    allowed_children=("Name", "Logo", "Bio", "Cover"),
)

_NAME = BlockDef(
    name="Name",
    parent="Profile",
    repeatable=False,
    properties=_properties(
        PropertyDef("title", ValueType.STRING, "", required=True),
        PropertyDef("subtitle", ValueType.STRING, ""),
        PropertyDef(
            "align",
            ValueType.ENUM,
            "center",
            enum_values=("left", "center", "right"),
        ),
        PropertyDef("titleColor", ValueType.COLOR, "#000000"),
        PropertyDef("subColor", ValueType.COLOR, "#000000"),
    ),
)

_LOGO = BlockDef(
    name="Logo",
    parent="Profile",
    repeatable=False,
    properties=_properties(
        PropertyDef("image", ValueType.IMAGE, "", required=True),
        PropertyDef(
            "shape",
            ValueType.ENUM,
            "circle",
            enum_values=("circle", "square"),
        ),
        PropertyDef("borderColor", ValueType.COLOR, "transparent"),
    ),
)

_BIO = BlockDef(
    name="Bio",
    parent="Profile",
    repeatable=False,
    properties=_properties(
        PropertyDef("text", ValueType.STRING, "", required=True),
        PropertyDef(
            "align",
            ValueType.ENUM,
            "center",
            enum_values=("left", "center", "right"),
        ),
        PropertyDef("textColor", ValueType.COLOR, "#000000"),
        PropertyDef("backgroundColor", ValueType.COLOR, "transparent"),
        PropertyDef("borderColor", ValueType.COLOR, "transparent"),
        PropertyDef(
            "shape",
            ValueType.ENUM,
            "rounded",
            enum_values=("sharp", "slightlyRounded", "rounded", "pill"),
        ),
    ),
)

_COVER = BlockDef(
    name="Cover",
    parent="Profile",
    repeatable=False,
    properties=_properties(
        PropertyDef("image", ValueType.IMAGE, "", required=True),
        PropertyDef(
            "shape",
            ValueType.ENUM,
            "rounded",
            enum_values=("rectangle", "rounded"),
        ),
    ),
)

_TITLE = BlockDef(
    name="Title",
    parent=None,
    repeatable=True,
    properties=_properties(
        PropertyDef("title", ValueType.STRING, "", required=True),
        PropertyDef(
            "align",
            ValueType.ENUM,
            "center",
            enum_values=("left", "center", "right"),
        ),
        PropertyDef("titleColor", ValueType.COLOR, "#000000"),
    )
)

_TEXT = BlockDef(
    name="Text",
    parent=None,
    repeatable=True,
    properties=_properties(
        PropertyDef("text", ValueType.STRING, "", required=True),
        PropertyDef(
            "align",
            ValueType.ENUM,
            "center",
            enum_values=("left", "center", "right"),
        ),
        PropertyDef("textColor", ValueType.COLOR, "#000000"),
        PropertyDef("backgroundColor", ValueType.COLOR, "transparent"),
        PropertyDef("borderColor", ValueType.COLOR, "transparent"),
        PropertyDef(
            "shape",
            ValueType.ENUM,
            "rounded",
            enum_values=("sharp", "slightlyRounded", "rounded", "pill"),
        ),
    ),
)

_SOCIAL_MEDIA_PLATFORMS = (
    "instagram",
    "telegram",
    "youtube",
    "tiktok",
    "x",
    "linkedin",
    "github",
    "spotify",
    "twitch",
    "pinterest",
    "facebook",
    "patreon",
)

_SOCIAL_NETWORK_PLATFORMS = (
    "telegram",
    "whatsapp",
    "discord",
    "skype",
    "line",
    "viber",
    "kik",
    "facebookMessenger",
    "bale",
    "eitaa",
    "rubika",
)

_SOCIALMEDIA = BlockDef(
    name="SocialMedia",
    parent=None,
    repeatable=True,
    allowed_children=("SocialMediaItem",),
    properties=_properties(
        PropertyDef("columns", ValueType.NUMBER, 1),
        PropertyDef("showTitle", ValueType.BOOLEAN, True),
        PropertyDef("showIcon", ValueType.BOOLEAN, True),
        PropertyDef(
            "iconPosition",
            ValueType.ENUM,
            "right",
            enum_values=("left", "right"),
        ),
        PropertyDef(
            "itemsOrder",
            ValueType.ENUM,
            "rtl",
            enum_values=("ltr", "rtl"),
        ),
        PropertyDef("titleColor", ValueType.COLOR, "#1A1A1A"),
        PropertyDef("iconColor", ValueType.COLOR, ""),
        PropertyDef("backgroundColor", ValueType.COLOR, ""),
        PropertyDef("borderColor", ValueType.COLOR, "transparent"),
        PropertyDef(
            "shape",
            ValueType.ENUM,
            "rounded",
            enum_values=("sharp", "slightlyRounded", "rounded", "pill"),
        ),
    ),
)

_SOCIALMEDIA_ITEM = BlockDef(
    name="SocialMediaItem",
    parent="SocialMedia",
    repeatable=True,
    properties=_properties(
        PropertyDef(
            "service",
            ValueType.ENUM,
            "",
            enum_values=_SOCIAL_MEDIA_PLATFORMS,
            required=True,
        ),
        PropertyDef("title", ValueType.STRING, ""),
        PropertyDef("url", ValueType.URL, "", required=True),
        PropertyDef("titleColor", ValueType.COLOR, ""),
        PropertyDef("iconColor", ValueType.COLOR, ""),
        PropertyDef("backgroundColor", ValueType.COLOR, ""),
        PropertyDef("borderColor", ValueType.COLOR, ""),
    ),
)

_SOCIALNETWORK = BlockDef(
    name="SocialNetwork",
    parent=None,
    repeatable=True,
    allowed_children=("SocialNetworkItem",),
    properties=_properties(
        PropertyDef("columns", ValueType.NUMBER, 1),
        PropertyDef("showTitle", ValueType.BOOLEAN, True),
        PropertyDef("showIcon", ValueType.BOOLEAN, True),
        PropertyDef(
            "iconPosition",
            ValueType.ENUM,
            "right",
            enum_values=("left", "right"),
        ),
        PropertyDef(
            "itemsOrder",
            ValueType.ENUM,
            "rtl",
            enum_values=("ltr", "rtl"),
        ),
        PropertyDef("titleColor", ValueType.COLOR, "#3B3B3B"),
        PropertyDef("iconColor", ValueType.COLOR, ""),
        PropertyDef("backgroundColor", ValueType.COLOR, ""),
        PropertyDef("borderColor", ValueType.COLOR, "transparent"),
        PropertyDef(
            "shape",
            ValueType.ENUM,
            "rounded",
            enum_values=("sharp", "slightlyRounded", "rounded", "pill"),
        ),
    ),
)

_SOCIALNETWORK_ITEM = BlockDef(
    name="SocialNetworkItem",
    parent="SocialNetwork",
    repeatable=True,
    properties=_properties(
        PropertyDef(
            "service",
            ValueType.ENUM,
            "",
            enum_values=_SOCIAL_NETWORK_PLATFORMS,
            required=True,
        ),
        PropertyDef("title", ValueType.STRING, ""),
        PropertyDef("url", ValueType.URL, "", required=True),
        PropertyDef("titleColor", ValueType.COLOR, ""),
        PropertyDef("iconColor", ValueType.COLOR, ""),
        PropertyDef("backgroundColor", ValueType.COLOR, ""),
        PropertyDef("borderColor", ValueType.COLOR, ""),
    ),
)

_ADDRESS_SERVICES = ("googleMap", "waze", "neshan", "balad")

_CONTACT_TYPES = ("mobile", "phone", "email", "sms", "website")

_CONTACT = BlockDef(
    name="Contact",
    parent=None,
    repeatable=True,
    allowed_children=("ContactItem",),
    properties=_properties(
        PropertyDef("columns", ValueType.NUMBER, 1),
        PropertyDef("showTitle", ValueType.BOOLEAN, True),
        PropertyDef("showIcon", ValueType.BOOLEAN, True),
        PropertyDef(
            "iconPosition",
            ValueType.ENUM,
            "right",
            enum_values=("left", "right"),
        ),
        PropertyDef(
            "itemsOrder",
            ValueType.ENUM,
            "rtl",
            enum_values=("ltr", "rtl"),
        ),
        PropertyDef("titleColor", ValueType.COLOR, "#00B4B0"),
        PropertyDef("iconColor", ValueType.COLOR, "#00B4B0"),
        PropertyDef("backgroundColor", ValueType.COLOR, "#FFFFFF"),
        PropertyDef("borderColor", ValueType.COLOR, "#00B4B0"),
        PropertyDef(
            "shape",
            ValueType.ENUM,
            "rounded",
            enum_values=("sharp", "slightlyRounded", "rounded", "pill"),
        ),
    ),
)

_CONTACT_ITEM = BlockDef(
    name="ContactItem",
    parent="Contact",
    repeatable=True,
    properties=_properties(
        PropertyDef(
            "service",
            ValueType.ENUM,
            "",
            enum_values=_CONTACT_TYPES,
            required=True,
        ),
        PropertyDef("title", ValueType.STRING, ""),
        PropertyDef("value", ValueType.STRING, "", required=True),
        PropertyDef("titleColor", ValueType.COLOR, ""),
        PropertyDef("iconColor", ValueType.COLOR, ""),
        PropertyDef("backgroundColor", ValueType.COLOR, ""),
        PropertyDef("borderColor", ValueType.COLOR, ""),
    ),
)

_ADDRESS = BlockDef(
    name="Address",
    parent=None,
    repeatable=True,
    allowed_children=("AddressItem",),
    properties=_properties(
        PropertyDef("address", ValueType.STRING, ""),
        PropertyDef("addressColor", ValueType.COLOR, "#000000"),
        PropertyDef("columns", ValueType.NUMBER, 1),
        PropertyDef("showTitle", ValueType.BOOLEAN, True),
        PropertyDef("showIcon", ValueType.BOOLEAN, True),
        PropertyDef(
            "iconPosition",
            ValueType.ENUM,
            "right",
            enum_values=("left", "right"),
        ),
        PropertyDef(
            "itemsOrder",
            ValueType.ENUM,
            "rtl",
            enum_values=("ltr", "rtl"),
        ),
        PropertyDef("titleColor", ValueType.COLOR, "#3B3B3B"),
        PropertyDef("iconColor", ValueType.COLOR, ""),
        PropertyDef("backgroundColor", ValueType.COLOR, ""),
        PropertyDef("borderColor", ValueType.COLOR, "transparent"),
        PropertyDef(
            "shape",
            ValueType.ENUM,
            "rounded",
            enum_values=("sharp", "slightlyRounded", "rounded", "pill"),
        ),
    ),
)

_ADDRESS_ITEM = BlockDef(
    name="AddressItem",
    parent="Address",
    repeatable=True,
    properties=_properties(
        PropertyDef(
            "service",
            ValueType.ENUM,
            "",
            enum_values=_ADDRESS_SERVICES,
            required=True,
        ),
        PropertyDef("title", ValueType.STRING, ""),
        PropertyDef("url", ValueType.URL, "", required=True),
        PropertyDef("titleColor", ValueType.COLOR, ""),
        PropertyDef("iconColor", ValueType.COLOR, ""),
        PropertyDef("backgroundColor", ValueType.COLOR, ""),
        PropertyDef("borderColor", ValueType.COLOR, ""),
    ),
)


#: The full set of blocks known to the compiler, keyed by block name.
BLOCKS: dict[str, BlockDef] = {
    _PROFILE.name: _PROFILE,
    _NAME.name: _NAME,
    _LOGO.name: _LOGO,
    _BIO.name: _BIO,
    _COVER.name: _COVER,
    _LINK.name: _LINK,
    _TITLE.name: _TITLE,
    _TEXT.name: _TEXT,
    _SOCIALMEDIA.name: _SOCIALMEDIA,
    _SOCIALMEDIA_ITEM.name: _SOCIALMEDIA_ITEM,
    _SOCIALNETWORK.name: _SOCIALNETWORK,
    _SOCIALNETWORK_ITEM.name: _SOCIALNETWORK_ITEM,
    _CONTACT.name: _CONTACT,
    _CONTACT_ITEM.name: _CONTACT_ITEM,
    _ADDRESS.name: _ADDRESS,
    _ADDRESS_ITEM.name: _ADDRESS_ITEM,
}


def get_block(name: str) -> Optional[BlockDef]:
    return BLOCKS.get(name)
