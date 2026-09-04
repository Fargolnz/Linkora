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


# ---------------------------------------------------------------------------
# Jalali (Shamsi) calendar conversion, based on the well-known jalaali-js
# algorithm. Used to convert a Persian countdown date into a Gregorian epoch.
# ---------------------------------------------------------------------------

#: Leap/jump boundaries of the Jalali calendar, indexed by Jalali year.
_JALALI_BREAKS = (-61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210, 1635, 2060)


def _div(a: int, b: int) -> int:
    """Integer division truncated toward zero, matching JavaScript ``~~(a / b)``."""
    q = a // b
    if q < 0 and q * b != a:
        q += 1
    return q


def _mod(a: int, b: int) -> int:
    return a - b * _div(a, b)


def _jal_cal(jy: int) -> tuple[int, int, int]:
    """Return ``(gy, march, leap_j)`` for a Jalali year ``jy``."""
    breaks = _JALALI_BREAKS
    bl = len(breaks)
    gy = jy + 621
    leap_j = -14
    jp = breaks[0]
    if jy < jp or jy >= breaks[bl - 1]:
        raise ValueError(f"invalid Jalali year: {jy}")
    jump = 0
    for i in range(1, bl):
        jm = breaks[i]
        jump = jm - jp
        if jy < jm:
            break
        leap_j += _div(jump, 33) * 8 + _div(_mod(jump, 33), 4)
        jp = jm
    n = jy - jp
    leap_j += _div(n, 33) * 8 + _div(_mod(n, 33) + 3, 4)
    if _mod(jump, 33) == 4 and jump - n == 4:
        leap_j += 1
    leap_g = _div(gy, 4) - _div((_div(gy, 100) + 1) * 3, 4) - 150
    march = 20 + leap_j - leap_g
    if _mod(jump, 33) == 4 and jump - n == 4:
        march += 1
    return gy, march, leap_j


def _g2d(gy: int, gm: int, gd: int) -> int:
    """Gregorian date to a fixed day number."""
    d = (_div((gy + _div(gm - 8, 6) + 100100) * 1461, 4)
         + _div(153 * _mod(gm + 9, 12) + 2, 5)
         + gd - 34840408)
    d = d - _div(_div(gy + 100100 + _div(gm - 8, 6), 100) * 3, 4) + 752
    return d


def _d2g(jdn: int) -> tuple[int, int, int]:
    """Fixed day number to a Gregorian date ``(gy, gm, gd)``."""
    j = 4 * jdn + 139361631
    j = j + _div(_div(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908
    i = _div(_mod(j, 1461), 4) * 5 + 308
    gd = _div(_mod(i, 153), 5) + 1
    gm = _mod(_div(i, 153), 12) + 1
    gy = _div(j, 1461) - 100100 + _div(8 - gm, 6)
    return gy, gm, gd


def _j2d(jy: int, jm: int, jd: int) -> int:
    """Jalali date to a fixed day number."""
    gy, march, _ = _jal_cal(jy)
    return _g2d(gy, 3, march) + (jm - 1) * 31 - _div(jm, 7) * (jm - 7) + jd - 1


def _jalali_year_length(jy: int) -> int:
    """Days in Jalali year ``jy`` (365, or 366 when it is a leap year)."""
    gy, march, _ = _jal_cal(jy)
    gy_next, march_next, _ = _jal_cal(jy + 1)
    return _g2d(gy_next, 3, march_next) - _g2d(gy, 3, march)


def is_jalali_date(value: object) -> bool:
    """True for a real Jalali (Shamsi) calendar date in ``yyyy/mm/dd`` form."""
    if not isinstance(value, str):
        return False
    match = _DATE_RE.match(value)
    if match is None:
        return False
    jy, jm, jd = (int(match.group(i)) for i in (1, 2, 3))
    if not 1 <= jm <= 12:
        return False
    try:
        year_length = _jalali_year_length(jy)
    except ValueError:
        return False
    if jm <= 6:
        if jd > 31:
            return False
        day_of_year = (jm - 1) * 31 + (jd - 1)
    else:
        if jd > 30:
            return False
        day_of_year = 186 + (jm - 7) * 30 + (jd - 1)
    return 0 <= day_of_year < year_length


def jalali_to_gregorian(year: int, month: int, day: int) -> tuple[int, int, int]:
    """Convert a Jalali date ``(year, month, day)`` to a Gregorian date."""
    return _d2g(_j2d(year, month, day))


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
