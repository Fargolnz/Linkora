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
_VIDEO_EXTENSIONS = (".mp4", ".webm", ".mov")


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


#: Date in yyyy/mm/dd form (used for a countdown target).
_DATE_RE = re.compile(r"^(\d{4})/(\d{1,2})/(\d{1,2})$")

#: Time in hh:mm 24-hour form (used for a countdown target).
_TIME_RE = re.compile(r"^(\d{1,2}):(\d{1,2})$")

_DAYS_IN_MONTH = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def _is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def is_date(value: object) -> bool:
    """True for a real calendar date in ``yyyy/mm/dd`` form.

    Rejects impossible dates such as ``2026/13/40`` while accepting single
    digit months and days like ``2026/9/4``.
    """
    if not isinstance(value, str):
        return False
    match = _DATE_RE.match(value)
    if match is None:
        return False
    year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
    if not 1 <= month <= 12:
        return False
    max_day = _DAYS_IN_MONTH[month]
    if month == 2 and _is_leap_year(year):
        max_day = 29
    return 1 <= day <= max_day


def is_time(value: object) -> bool:
    """True for a 24-hour ``hh:mm`` time value."""
    if not isinstance(value, str):
        return False
    match = _TIME_RE.match(value)
    if match is None:
        return False
    hour, minute = int(match.group(1)), int(match.group(2))
    return 0 <= hour <= 23 and 0 <= minute <= 59


_YOUTUBE_RE = re.compile(
    r"^https?://(?:(?:www\.)?youtube\.com/watch\?.*v=|youtu\.be/)[A-Za-z0-9_-]+"
)
_APARAT_RE = re.compile(
    r"^https?://(?:www\.)?aparat\.com/v/[A-Za-z0-9_-]+"
)


def is_video_url(value: object) -> bool:
    """True for a YouTube, Aparat, or local video file URL/path."""
    if not isinstance(value, str) or not value.strip():
        return False
    lower = value.lower()
    if _YOUTUBE_RE.match(value):
        return True
    if _APARAT_RE.match(value):
        return True
    if is_file_path(value):
        return any(lower.endswith(ext) for ext in _VIDEO_EXTENSIONS)
    if _URL_RE.match(value):
        return any(lower.endswith(ext) for ext in _VIDEO_EXTENSIONS)
    return False
