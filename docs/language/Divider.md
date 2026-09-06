# ➖ Divider

## Description

The `Divider` block renders an ornamental separator between sections of the page. It embeds a hand-drawn SVG artwork that stretches across the full width of the card and is recolored to match the page's accent color.

Five distinct ornament styles are available, each with its own silhouette: `orb`, `beads`, `diamond`, `bloom`, and `grace`. The divider is purely decorative — it carries no text and links, and requires no JavaScript.

The `Divider` block always requires a `style`.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | None |
| Repeatable | ✅ Yes |

Multiple `Divider` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Style | `style` | Enum | *(required)* | `orb`, `beads`, `diamond`, `bloom`, `grace` |
| Margin Top | `marginTop` | Number | `20` | Integer 8 – 200 |
| Margin Bottom | `marginBottom` | Number | `20` | Integer 8 – 200 |
| Color | `color` | Color | `#00B4B0` | Valid Color |

---

## Property Details

### `style`

Selects which of the five ornament designs is rendered.

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ✅ Yes |
| Default | *(none — must be provided)* |

Supported values:

| Value | Description |
|-------|-------------|
| `orb` | A thin double line broken by a single circular orb |
| `beads` | A thin double line threaded with small bead dots |
| `diamond` | A line adorned with diamond-shaped facets |
| `bloom` | A line that blossoms into a floral centerpiece |
| `grace` | A single elegant curved sweep |

---

### `marginTop`

Defines the space above the divider.

| Field | Value |
|-------|-------|
| Type | Number |
| Required | ❌ No |
| Default | `20` |
| Allowed Range | Integer 8 – 200 |

---

### `marginBottom`

Defines the space below the divider.

| Field | Value |
|-------|-------|
| Type | Number |
| Required | ❌ No |
| Default | `20` |
| Allowed Range | Integer 8 – 200 |

---

### `color`

Defines the color of the divider artwork. Because the SVG is drawn with `currentColor`, the whole ornament takes on this color.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#00B4B0` |

---

## Semantic Rules

The compiler performs the following semantic validations on the `Divider` block:

- The `style` property is mandatory.
- `style` must be one of `orb`, `beads`, `diamond`, `bloom`, or `grace`.
- `marginTop` and `marginBottom` must be integers between 8 and 200 (inclusive), when provided.
- `color` must be a valid color value.
- Unknown or duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.

---

## Rendering

- Each divider renders as a full-width wrapper element holding the selected inline SVG.
- The SVG scales to any screen width while preserving its design's aspect ratio.
- The artwork inherits its stroke and fill from the `color` property.
- A divider adds no text, links, or blocking scripts — it is purely a visual separator.
- Margins apply vertically around the divider to space it from neighboring blocks.

---

## Examples

### Minimal Example

The style is the only required property:

```lkr
Divider { style: orb }
```

---

### Five Styles

```lkr
Divider { style: orb }
Divider { style: beads }
Divider { style: diamond }
Divider { style: bloom }
Divider { style: grace }
```

---

### Customized Example

```lkr
Divider {
    style: bloom
    marginTop: 40
    marginBottom: 40
    color: "#C7006E"
}
```

---

## Invalid Examples

Missing required `style` property:

```lkr
Divider { }
```

❌ Missing required property `style`.

---

Unknown style value:

```lkr
Divider { style: zigzag }
```

❌ `style` must be one of the predefined values.

---

Margin outside the allowed range:

```lkr
Divider { style: orb, marginTop: 400 }
```

❌ `marginTop` must be an integer between 8 and 200 (inclusive).

---

## Notes

💡 The `Divider` block is purely decorative: it adds no text, links, focusable elements, or scripts.

💡 The artwork is inlined as an SVG inside the compiled HTML, so no external image files are needed and the divider always renders.

💡 The divider is a top-level block and cannot be nested inside other blocks.