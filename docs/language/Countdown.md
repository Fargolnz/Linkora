# ⏳ Countdown

## Description

The `Countdown` block displays a live countdown timer to a specific event date and time. It renders four boxes showing the remaining **days**, **hours**, **minutes**, and **seconds**, each with a unit label underneath.

The timer updates every second in the browser via an embedded JavaScript script. Once the target moment passes, the digits freeze at `00` and an optional custom message (`expiredText`) appears below the timer.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Repeatable | ✅ Yes |

Multiple `Countdown` blocks may appear within the same document. A single shared script drives all of them.

---

## Properties

| Property | Keyword | Type | Default | Required |
|----------|---------|------|---------|:--------:|
| Date | `date` | Date | — | ✅ Yes |
| Time | `time` | Time | — | ✅ Yes |
| Calendar | `calendar` | Enum | `jalali` | ❌ No |
| Expired Message | `expiredText` | String | `""` | ❌ No |
| Label Language | `language` | Enum | `fa` | ❌ No |
| Text Color | `textColor` | Color | `#00B4B0` | ❌ No |
| Background Color | `backgroundColor` | Color | `transparent` | ❌ No |
| Border Color | `borderColor` | Color | `transparent` | ❌ No |
| Shape | `shape` | Enum | `rounded` | ❌ No |

---

## Property Details

### `date`

The target date of the countdown, in `yyyy/mm/dd` form, interpreted according to the `calendar` property. With the default `jalali` calendar the value must be a real Jalali (Persian) date — for example `1405/09/15`; impossible dates such as `1404/07/31` (Mehr has only 30 days) are rejected. With `calendar: gregorian` the value must be a real Gregorian date instead; impossible dates such as `2026/13/40` are rejected, and single-digit months and days are accepted (e.g. `2026/9/4`).

| Field | Value |
|-------|-------|
| Type | Date |
| Required | ✅ Yes |

---

### `time`

The target time of the countdown, in 24-hour `hh:mm` form (hours `0–23`, minutes `0–59`).

| Field | Value |
|-------|-------|
| Type | Time |
| Required | ✅ Yes |

---

### `calendar`

Selects the calendar used to interpret the `date` value.

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ❌ No |
| Default | `jalali` |

Supported values:

| Value | Date Format | Example |
|-------|-------------|---------|
| `jalali` | Jalali (Shamsi, Persian) `yyyy/mm/dd` | `1404/09/15` |
| `gregorian` | Gregorian `yyyy/mm/dd` | `2026/09/15` |

`jalali` is the default, so Persian users can type their date directly in the Shamsi calendar — the `date` is interpreted as a Persian date and converted to the corresponding Gregorian moment at compile time, without needing to set anything. With `calendar: gregorian`, the `date` is interpreted as a Gregorian date instead. Impossible dates (such as `1404/07/31`, since Mehr has 30 days) are rejected.

---

### `expiredText`

An optional message shown below the countdown **only after** the target moment passes. When empty, no message appears — the timer simply shows all zeros.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

---

### `language`

Selects the language of the unit labels below the digits. In `fa` mode the numbers are also rendered using Persian digits (۰ ۱ … ۹).

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ❌ No |
| Default | `fa` |

Supported values:

| Value | Labels | Digits |
|-------|--------|--------|
| `fa` | روز، ساعت، دقیقه، ثانیه | Persian (۰–۹) |
| `en` | Days, Hours, Minutes, Seconds | ASCII (0–9) |

---

### `textColor`

Defines the color of the countdown digits and labels.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#00B4B0` |

---

### `backgroundColor`

Defines the background fill of the countdown card. When set to `transparent` (the default), the card has no background.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `transparent` |

---

### `borderColor`

Defines the border color around the countdown card.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `transparent` |

---

### `shape`

Defines the corner shape of the countdown card.

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ❌ No |
| Default | `rounded` |

Supported values:

| Value | Description |
|-------|-------------|
| `sharp` | Sharp rectangular corners |
| `slightlyRounded` | Small corner radius |
| `rounded` | Standard rounded corners |
| `pill` | Fully rounded pill-shaped box |

---

## Semantic Rules

The compiler performs the following semantic validations on the `Countdown` block:

- `date` must be a real date in `yyyy/mm/dd` form; it is validated against the Jalali (Persian) calendar by default and against the Gregorian calendar when `calendar: gregorian` is set.
- `time` must be a valid 24-hour time in `hh:mm` form.
- `calendar` must be one of `gregorian` or `jalali`.
- `language` must be one of `fa` or `en`.
- `textColor`, `backgroundColor`, and `borderColor` must be valid hex colors or `transparent`.
- `shape` must be one of the predefined enum values.
- Both `date` and `time` are required.
- Unknown or duplicate properties are not allowed.

---

## Rendering Behavior

The `Countdown` block renders a card containing a row of four boxes:

| Box | Content |
|-----|---------|
| Days | Number of full days remaining |
| Hours | Remaining hours (0–23) |
| Minutes | Remaining minutes (0–59) |
| Seconds | Remaining seconds (0–59) |

Each box shows a two-digit number with its unit label underneath.

- The target moment is embedded as a `data-target` attribute (an epoch timestamp in milliseconds).
- A single shared JavaScript script ticks every second and updates all countdown digits.
- When the target moment passes, the boxes freeze at `00` and the `expiredText` message (if set) is revealed below.
- With a transparent background, the card has no visible box fill; a background color turns it into a filled card, optionally with a border and a corner `shape`.

---

## Examples

### Simple Persian Example

```lkr
Countdown {
    date: "1405/09/15"
    time: "23:59"
}
```

Since `jalali` is the default calendar, a Persian date needs no extra properties.

---

### English Example with Message

```lkr
Countdown {
    date: "2026/07/04"
    time: "14:00"
    language: en
    expiredText: "The event has started!"
    calendar: gregorian
}
```

---

### Jalali (Persian) Example

```lkr
Countdown {
    date: "1405/09/15"
    time: "12:00"
    calendar: jalali
    language: fa
    expiredText: "رویداد آغاز شد!"
}
```

---

### Customized Example

```lkr
Countdown {
    date: "2026/09/15"
    time: "09:30"
    calendar: gregorian
    textColor: "#FFFFFF"
    backgroundColor: "#1E1E1E"
    borderColor: "#00B4B0"
    shape: pill
}
```

---

## Invalid Examples

Missing required `date` property:

```lkr
Countdown {
    time: "23:59"
}
```

❌ Missing required property `date`.

---

Impossible Gregorian date:

```lkr
Countdown { date: "2026/13/40", time: "23:59", calendar: gregorian }
```

❌ `date` must be a real Gregorian date in `yyyy/mm/dd` form.

---

Impossible Jalali date (Mehr has only 30 days):

```lkr
Countdown { date: "1405/07/31", time: "23:59", calendar: jalali }
```

❌ `date` must be a real Jalali (Shamsi) date in `yyyy/mm/dd` form.

---

Out-of-range time:

```lkr
Countdown { date: "2026/12/31", time: "25:00", calendar: gregorian }
```

❌ `time` must be a valid 24-hour time in `hh:mm` form.

---

Invalid language:

```lkr
Countdown { date: "2026/12/31", time: "23:59", language: de, calendar: gregorian }
```

❌ `language` must be one of `fa`, `en`.

---

## Notes

💡 The timer is live: it updates every second while the page is open, with no page reload needed.

💡 The server-side HTML is deterministic (digits start at `00`, or `۰۰` in `fa` mode); the embedded script computes and displays the correct remaining time immediately on page load.

💡 `date` and `time` are required — there is no default event moment. Specify the exact target every time.

💡 Persian users can type the date directly in the Shamsi calendar (for example `1404/09/15`) — `jalali` is the default calendar, and the compiler converts it to the correct Gregorian moment automatically. Set `calendar: gregorian` for Gregorian dates.

💡 Multiple `Countdown` blocks share a single script, so adding more timers costs no extra JavaScript.