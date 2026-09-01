# 🖼️ Image

## Description

The `Image` block renders a gallery of display cards, each showing a picture with an optional caption. It supports two display modes: a responsive grid (`single`) and a pure-CSS scroll-snap carousel (`slider`).

It serves as a container for `ImageItem` children. Every child renders one image card with an optional `title` and `description`, and inherits its visual styling (colors, shape, shadow) from the container.

The `Image` block always requires at least one child `ImageItem`.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | `ImageItem` |
| Repeatable | ✅ Yes |

Multiple `Image` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Display Mode | `displayMode` | Enum | `single` | `single`, `slider` |
| Columns | `columns` | Number | `1` | `1`, `2` |
| Title Color | `titleColor` | Color | `#000000` | Valid Color |
| Description Color | `descriptionColor` | Color | `#3B3B3B` | Valid Color |
| Background Color | `backgroundColor` | Color | `#FFFFFF` | Valid Color |
| Border Color | `borderColor` | Color | `transparent` | Valid Color |
| Shape | `shape` | Enum | `rounded` | `sharp`, `slightlyRounded`, `rounded`, `pill` |
| Image Shadow | `imageShadow` | Boolean | `false` | `true`, `false` |

---

## Property Details

### `displayMode`

Selects how the image cards are arranged.

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ❌ No |
| Default | `single` |

Supported values:

- `single` — cards are laid out in a responsive grid.
- `slider` — cards are placed in a horizontal, scroll-snap carousel (one card visible per view) with a bottom dot indicator overlaid on the image.

---

### `columns`

Controls how many cards appear in each row of the grid.

| Field | Value |
|-------|-------|
| Type | Number |
| Required | ❌ No |
| Default | `1` |

Supported values: `1`, `2`.

> ⚠️ `columns` applies only in `single` display mode and is ignored (without error) in `slider` mode.

---

### `titleColor`

Defines the default color of the card title text.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#000000` |

---

### `descriptionColor`

Defines the default color of the card description text.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#3B3B3B` |

---

### `backgroundColor`

Defines the default background color of each card.

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

Defines the default corner shape of each card.

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

### `imageShadow`

Controls whether the image receives a soft drop shadow.

| Field | Value |
|-------|-------|
| Type | Boolean |
| Required | ❌ No |
| Default | `false` |

---

## Semantic Rules

The compiler performs the following semantic validations on the `Image` block:

- In `single` display mode, `columns` must be `1` or `2`.
- In `slider` display mode, `columns` is ignored and not validated.
- The block must contain at least one `ImageItem` child.
- Unknown or duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.
- Color properties must contain valid color values.

---

## Children

### ImageItem

An `ImageItem` renders a single display card inside the container.

#### Hierarchy

| Property | Value |
|----------|-------|
| Parent | `Image` |
| Repeatable | ✅ Yes |

#### Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Image | `image` | Image | `""` (required) | Any valid image path/URL |
| Title | `title` | String | `""` | Any valid string |
| Description | `description` | String | `""` | Any valid string |
| Alt | `alt` | String | `""` | Any valid string |
| Title Color | `titleColor` | Color | `""` (inherited) | Valid Color |
| Description Color | `descriptionColor` | Color | `""` (inherited) | Valid Color |
| Background Color | `backgroundColor` | Color | `""` (inherited) | Valid Color |
| Border Color | `borderColor` | Color | `""` (inherited) | Valid Color |

Item-level color properties that are omitted inherit their value from the parent `Image` block, and fall back to the parent defaults if the parent does not define them.

#### Required Properties

The following property is mandatory on every `ImageItem`:

- `image`

Failure to provide it results in a semantic validation error.

#### Property Details

##### `image`

The picture to display. It can be a local file path or an external URL.

| Field | Value |
|-------|-------|
| Type | Image |
| Required | ✅ Yes |
| Default | none |

Local files referenced here are automatically copied into the output directory at compile time.

---

##### `title`

An optional caption title shown below the image.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

---

##### `description`

An optional caption description shown below the title.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

---

##### `alt`

Alternative text for the image.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

When omitted, the `title` (or `description`) is used, falling back to a generic `Image` label.

---

##### `titleColor`, `descriptionColor`, `backgroundColor`, `borderColor`

These visual properties behave like their `Image` counterparts but apply only to the individual card. When omitted, they inherit the parent block's value.

| Property | Type | Inherits |
|----------|------|----------|
| `titleColor` | Color | Parent `titleColor` |
| `descriptionColor` | Color | Parent `descriptionColor` |
| `backgroundColor` | Color | Parent `backgroundColor` |
| `borderColor` | Color | Parent `borderColor` |

---

## Rendering Behavior

The `Image` block renders each child as a display card containing the image followed by an optional caption block:

- In `single` mode, cards are grouped into rows of `columns` each.
- Caption space is reserved **per row**: a row reserves equal caption space for every card in it only when at least one card in that row has a caption. Rows where no card has a caption leave no caption space, keeping the cards as pure images.
- In `slider` mode, cards are placed in a horizontal scroll-snap carousel (one card per view) with a light dot indicator overlaid at the bottom edge of the image: one dot per slide, the current slide filled and the rest empty outlines. The dots highlight live while swiping and jump to a slide on tap (backed by a small embedded script).
- Each card's corner shape follows `shape`, and the image is always cropped to a consistent ratio (`aspect-ratio`) with `object-fit: cover`.
- `imageShadow` adds a soft drop shadow to the image.
- Color defaults are applied at the container level and inherited by each item.

---

## Examples

### Minimal Example

```lkr
Image {

    ImageItem { image: "./assets/photo1.jpg" }
    ImageItem { image: "./assets/photo2.jpg" }

}
```

---

### Customized Example

```lkr
Image {

    columns: 2

    displayMode: single

    shape: slightlyRounded

    imageShadow: true

    titleColor: "#111111"

    descriptionColor: "#4B5563"

    backgroundColor: "#FFFFFF"

    borderColor: "#E5E7EB"

    ImageItem { image: "./assets/photo1.jpg", title: "Beach", description: "A sunny afternoon" }
    ImageItem { image: "./assets/photo2.jpg", description: "The old town" }
    ImageItem { image: "./assets/photo3.jpg", title: "Mountains" }
    ImageItem { image: "./assets/photo4.jpg" }

}
```

---

### Slider Example

```lkr
Image {

    displayMode: slider

    shape: rounded

    ImageItem { image: "./assets/photo1.jpg", title: "Slide One", description: "First highlight" }
    ImageItem { image: "./assets/photo2.jpg", title: "Slide Two" }
    ImageItem { image: "./assets/photo3.jpg" }

}
```

---

### Custom Item Colors

```lkr
Image {

    titleColor: "#FFFFFF"

    descriptionColor: "#DDDDDD"

    backgroundColor: "#1F2937"

    ImageItem { image: "./assets/photo1.jpg", title: "Dark card", description: "Inherited colors" }

}
```

---

## Invalid Examples

Missing required `image` property:

```lkr
Image {
    ImageItem { }
}
```

❌ Missing required property `image`.

---

Invalid `columns` value in `single` mode:

```lkr
Image {
    columns: 3
    ImageItem { image: "./assets/photo1.jpg" }
}
```

❌ In single display mode `columns` must be one of 1, 2.

---

No children:

```lkr
Image {
}
```

❌ The block must contain at least one `ImageItem` child.

---

Invalid `displayMode`:

```lkr
Image {
    displayMode: carousel
    ImageItem { image: "./assets/photo1.jpg" }
}
```

❌ `displayMode` is not a valid value.

---

## Notes

💡 The `Image` block displays static content cards and is not interactive — `ImageItem` has no `url`.

💡 For the neatest result, use a uniform number of captions per row: when some cards in a row have captions and others do not, the empty cards still reserve equal caption space so the row stays aligned.

💡 Local images are copied automatically at compile time, so you only need to reference them by their relative path.
