# 🪧 Banner

## Description

The `Banner` block renders a grid of linked image cards. Each card displays an image with an always-visible dark gradient overlay showing a title and description. The entire card is clickable, linking to the specified URL.

It serves as a container for `BannerItem` children. Every child represents one promotional or informational card with an image, text overlay, and a link. The grid adapts to the number of columns you specify and is fully customizable through container-level properties that children can inherit.

The `Banner` block always requires at least one child `BannerItem`.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | `BannerItem` |
| Repeatable | ✅ Yes |

Multiple `Banner` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Columns | `columns` | Number | `1` | `1`, `2` |
| Title Color | `titleColor` | Color | `#FFFFFF` | Valid Color |
| Description Color | `descriptionColor` | Color | `#FFFFFF` | Valid Color |
| Border Color | `borderColor` | Color | `transparent` | Valid Color |
| Shape | `shape` | Enum | `rounded` | `sharp`, `slightlyRounded`, `rounded`, `pill` |

---

## Property Details

### `columns`

Controls how many cards appear in each row of the grid.

| Field | Value |
|-------|-------|
| Type | Number |
| Required | ❌ No |
| Default | `1` |

Supported values: `1`, `2`.

---

### `titleColor`

Defines the default color of the card title text shown on the overlay.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#FFFFFF` |

---

### `descriptionColor`

Defines the default color of the card description text shown on the overlay.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#FFFFFF` |

---

### `borderColor`

Defines the default border color around each card.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `transparent` |

---

### `shape`

Defines the corner shape of each card.

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

The compiler performs the following semantic validations on the `Banner` block:

- `columns` must be `1` or `2`.
- The block must contain at least one `BannerItem` child.
- Unknown or duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.
- Color properties must contain valid color values.

---

## Children

### BannerItem

A `BannerItem` renders a single linked image card inside the grid.

#### Hierarchy

| Property | Value |
|----------|-------|
| Parent | `Banner` |
| Repeatable | ✅ Yes |

#### Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Image | `image` | Image | `""` (required) | Any valid image path/URL |
| URL | `url` | URL | `""` (required) | Any valid URL |
| Title | `title` | String | `""` | Any valid string |
| Description | `description` | String | `""` | Any valid string |
| Title Color | `titleColor` | Color | `""` (inherited) | Valid Color |
| Description Color | `descriptionColor` | Color | `""` (inherited) | Valid Color |
| Border Color | `borderColor` | Color | `""` (inherited) | Valid Color |

Item-level color properties that are omitted inherit their value from the parent `Banner` block, and fall back to the parent defaults if the parent does not define them.

#### Required Properties

The following properties are mandatory on every `BannerItem`:

- `image`
- `url`

Failure to provide either of these results in a semantic validation error.

#### Property Details

##### `image`

The background picture for the banner card.

| Field | Value |
|-------|-------|
| Type | Image |
| Required | ✅ Yes |

Local files referenced here are automatically copied into the output directory at compile time.

---

##### `url`

The full URL the card links to. The entire card is wrapped in an anchor element pointing to this URL.

| Field | Value |
|-------|-------|
| Type | URL |
| Required | ✅ Yes |

---

##### `title`

An optional title shown on the dark gradient overlay at the bottom of the image.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

---

##### `description`

An optional description shown below the title on the overlay.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

---

##### `titleColor`, `descriptionColor`, `borderColor`

These visual properties behave like their `Banner` counterparts but apply only to the individual card. When omitted, they inherit the parent block's value.

| Property | Type | Inherits |
|----------|------|----------|
| `titleColor` | Color | Parent `titleColor` |
| `descriptionColor` | Color | Parent `descriptionColor` |
| `borderColor` | Color | Parent `borderColor` |

---

## Rendering Behavior

The `Banner` block renders each child as a clickable card:

- Cards are grouped into rows of `columns` each.
- Each card is wrapped in an `<a>` element linking to `url`, making the entire card a tap/click target.
- An image fills the card at a 16:9 aspect ratio with `object-fit: cover`.
- A dark gradient overlay sits at the bottom of the card, always showing the title and description.
- On hover (desktop), the card lifts slightly (`translateY(-2px)`) and dims — a subtle visual cue that the card is interactive.
- On mobile (touch devices), the card is fully tappable with no hover dependency.
- Color defaults are applied at the container level and inherited by each item.

---

## Examples

### Minimal Example

```lkr
Banner {
    BannerItem { image: "./assets/photo.jpg", url: "https://example.com" }
}
```

---

### Customized Example

```lkr
Banner {

    columns: 2

    shape: slightlyRounded

    titleColor: "#FFD700"

    descriptionColor: "#FFFFFF"

    borderColor: "#333333"

    BannerItem {
        image: "./assets/sale.jpg"
        url: "https://example.com/sale"
        title: "Summer Sale"
        description: "Up to 50% off on selected items."
        titleColor: "#FFFFFF"
    }
    BannerItem {
        image: "./assets/new.jpg"
        url: "https://example.com/new"
        title: "New Collection"
        description: "Check out the latest arrivals."
    }

}
```

---

### Single Column Example

```lkr
Banner {
    BannerItem {
        image: "./assets/hero.jpg"
        url: "https://example.com"
        title: "Welcome"
        description: "Explore our latest offerings."
    }
}
```

---

## Invalid Examples

Missing required `image` property:

```lkr
Banner {
    BannerItem { url: "https://example.com" }
}
```

❌ Missing required property `image`.

---

Missing required `url` property:

```lkr
Banner {
    BannerItem { image: "./assets/photo.jpg" }
}
```

❌ Missing required property `url`.

---

Invalid `columns` value:

```lkr
Banner {
    columns: 3
    BannerItem { image: "./assets/photo.jpg", url: "https://example.com" }
}
```

❌ `columns` must be one of 1, 2.

---

No children:

```lkr
Banner {
}
```

❌ The block must contain at least one `BannerItem` child.

---

## Notes

💡 The entire card is clickable — there is no separate button. The card wraps in a link to `url`.

💡 On desktop, hovering lifts the card slightly to signal interactivity. On mobile, the card is always tappable.

💡 The dark gradient overlay is always visible, ensuring title and description text remains readable over any image.
