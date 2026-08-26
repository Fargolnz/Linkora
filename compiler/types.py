"""Pure predicate functions used to validate property values.

Each function returns ``True`` when the given decoded value satisfies the
format requirements of the corresponding :class:`compiler.schema.ValueType`.
"""

from __future__ import annotations

import re

#: The special unquoted color value used for "no border".
TRANSPARENT_COLOR = "transparent"

#: Hex color: #RGB or #RRGGBB.
_HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?$")

#: HTTP/HTTPS URL requiring a host and an optional port/path.
_URL_RE = re.compile(
    r"^https?://[A-Za-z0-9](?:[A-Za-z0-9.-])*(?::[0-9]{1,5})?(?:[/?#][^\s]*)?$"
)


def is_color(value: object) -> bool:
    """True for a hex color or the special ``transparent`` value."""
    if not isinstance(value, str):
        return False
    return value == TRANSPARENT_COLOR or bool(_HEX_COLOR_RE.match(value))


def is_url(value: object) -> bool:
    """True for a well-formed HTTP/HTTPS URL."""
    return isinstance(value, str) and bool(_URL_RE.match(value))


def is_file_path(value: object) -> bool:
    """True for a plausible relative file path."""
    if not isinstance(value, str) or not value.strip():
        return False
    if value.startswith(("/", "\\")) or len(value) >= 2 and value[1] == ":":
        return False
    return not any(char.isspace() for char in value)


_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".svg", ".gif", ".webp")


def is_image(value: object) -> bool:
    """True for an HTTP/HTTPS URL or a relative file path with an image extension."""
    if not isinstance(value, str) or not value.strip():
        return False
    lower = value.lower()
    if _URL_RE.match(value):
        return any(lower.endswith(ext) for ext in _IMAGE_EXTENSIONS)
    if is_file_path(value):
        return any(lower.endswith(ext) for ext in _IMAGE_EXTENSIONS)
    return False


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_boolean(value: object) -> bool:
    return isinstance(value, bool)
