# 🔗 SuperLink

## Description

The `SuperLink` block renders a single, prominent link button used to showcase special or important links more conspicuously than a regular `Link`.

Unlike the `Link` block, a `SuperLink` can carry a short description and an icon alongside its title. It is a self-contained block — every SuperLink is one standalone button that redirects to an external webpage.

The appearance of the button is determined by its local properties or, when omitted, by the global theme defaults.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | None |
| Repeatable | ✅ Yes |

Multiple `SuperLink` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Link Title | `title` | String | `""` | Any valid string |
| Description | `description` | String | `""` | Any valid string |
| URL | `url` | URL | `""` | Valid HTTP/HTTPS URL |
| Icon | `icon` | Image | `""` | Valid image path/URL |
| Direction | `direction` | Enum | `rtl` | `ltr`, `rtl` |
| Title Color | `titleColor` | Color | `#FFFFFF` | Valid Color |
| Description Color | `descriptionColor` | Color | `#FFFFFF` | Valid Color |
| Icon Color | `iconColor` | Color | `#FFFFFF` | Valid Color |
| Background Color | `backgroundColor` | Color | `#00B4B0` | Valid Color |
| Border Color | `borderColor` | Color | `transparent` | Valid Color |
| Shape | `shape` | Enum | `rounded` | `sharp`, `slightlyRounded`, `rounded`, `pill` |

---

## Required Properties

The following `SuperLink` properties are mandatory:

- `title`
- `url`

Failure to provide either property results in a semantic validation error.

---

## Property Details

### `title`

Defines the main text (the link's heading) displayed inside the button.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ✅ Yes |

Example:

```lkr
title: "Visit My Portfolio"
```

---

### `description`

An optional short text shown below the title, such as a subtitle or a brief explanation of the link.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

When empty, the description line is not rendered at all, so no empty gap appears.

Example:

```lkr
description: "Browse my latest projects and case studies"
```

---

### `url`

Specifies the destination address opened when the button is clicked.

| Field | Value |
|-------|-------|
| Type | URL |
| Required | ✅ Yes |

Example:

```lkr
url: "https://example.com/portfolio"
```

---

### `icon`

An optional icon shown next to the title.

| Field | Value |
|-------|-------|
| Type | Image |
| Required | ❌ No |
| Default | `""` |

When `icon` is empty, a built-in "open link" arrow is drawn using `iconColor`. When a user-supplied icon is given (an image path or URL), it is displayed instead.

Local files referenced here are automatically copied into the output directory at compile time.

---

### `iconColor`

The color of the icon.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#FFFFFF` |

With the built-in icon, `iconColor` always tints the arrow.

With a user-supplied icon, the icon is **only** recolored when you explicitly set `iconColor`. If you do not set it, your icon is shown exactly as provided (its own colors are preserved).

---

### `direction`

Sets the reading direction of the block content and controls where the text and icon sit.

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ❌ No |
| Default | `rtl` |

Supported values:

| Value | Description |
|-------|-------------|
| `rtl` | Right-to-left (Persian) |
| `ltr` | Left-to-right (English) |

- **`ltr`**: the title and description are placed on the **left** side of the button and the icon on the **right**.
- **`rtl`**: the title and description are placed on the **right** side of the button and the icon on the **left**.

The text stack and the icon are anchored to opposite edges of the button, so the icon always sits on the trailing side of the reading direction.

---

### `titleColor`

Defines the color of the title text.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#FFFFFF` |

---

### `descriptionColor`

Defines the color of the description text.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#FFFFFF` |

The description text is always rendered at reduced emphasis: it is shown at `85%` opacity (`opacity: 0.85`), so even at the default white it appears slightly softer than the title and naturally reads as secondary without needing a different color.

---

### `backgroundColor`

Defines the background color of the button.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#00B4B0` |

---

### `borderColor`

Defines the color of the button border.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `transparent` |

---

### `shape`

Defines the corner shape of the button.

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

## Rendering Behavior

The `SuperLink` block renders a single clickable button:

- The entire block is wrapped in an `<a>` element linking to `url`.
- The text stack (title + optional description) and the icon are anchored to opposite edges of the button: text on the inline-start side, icon on the inline-end side.
- The button is taller than a standard `Link` (`min-height: 72px`) to accommodate the description.
- On hover (desktop), the button lifts slightly (`translateY(-2px)`) and dims — a subtle cue that it is interactive.
- On mobile, the button is fully tappable with no hover dependency.
- The description line is omitted entirely when `description` is empty, so an icon-only or title-only button stays tidy.
- Color defaults are applied the same way as the `Link` block.
- The `direction` property is written to the element as `data-direction`, and matching CSS toggles the reading direction — placing the text left and icon right for `ltr`, and text right and icon left for `rtl`.

---

## Examples

### Minimal Example

```lkr
Title { title: "Featured" }

SuperLink {
    title: "Visit My Portfolio"
    url: "https://example.com/portfolio"
}
```

---

### Customized Example (English, LTR)

```lkr
SuperLink {
    title: "Book a Consultation"
    description: "Free 30-minute introductory call"
    url: "https://example.com/book"
    icon: "./assets/calendar.svg"
    direction: ltr
    iconColor: "#00B4B0"
    titleColor: "#1F2937"
    descriptionColor: "#4B5563"
    backgroundColor: "#FFFFFF"
    borderColor: "#00B4B0"
    shape: pill
}
```

---

### Customized Example (Persian, RTL)

```lkr
SuperLink {
    title: "سفارش طراحی سایت"
    description: "مشاهده نمونه‌کارها و تعرفه‌ها"
    url: "https://example.com"
    iconColor: "#8B5CF6"
}
```

---

## Invalid Examples

Missing required `title` property:

```lkr
SuperLink { url: "https://example.com" }
```

❌ Missing required property `title`.

---

Missing required `url` property:

```lkr
SuperLink { title: "Go" }
```

❌ Missing required property `url`.

---

Invalid `direction` value:

```lkr
SuperLink {
    title: "Go"
    url: "https://example.com"
    direction: sideways
}
```

❌ `direction` must be one of `ltr`, `rtl`.

---

Invalid `shape` value:

```lkr
SuperLink {
    title: "Go"
    url: "https://example.com"
    shape: oval
}
```

❌ `shape` must be one of `sharp`, `slightlyRounded`, `rounded`, `pill`.

---

Unknown property:

```lkr
SuperLink {
    title: "Go"
    url: "https://example.com"
    fontSize: 18
}
```

❌ `fontSize` is not a property of the `SuperLink` block.

---

## Notes

💡 A `SuperLink` is best used for one or two standout links on the page, whereas `Link` is the everyday navigation button.

💡 The entire button is clickable — the whole block wraps in a link to `url`.

💡 A user-supplied icon keeps its original colors unless you explicitly set `iconColor`, in which case it is recolored to match.

💡 The `direction` property only affects the SuperLink block itself; set `direction: ltr` for an English button or leave the default `rtl` for Persian pages.
