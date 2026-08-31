# 📱 SocialMedia

## Description

The `SocialMedia` block renders a responsive grid of social-platform buttons, each linking out to a profile or page.

It serves as a container for `SocialMediaItem` children. Every child represents one platform button featuring its official brand icon and, optionally, a short label. The grid adapts to the number of columns you specify and is fully customizable through container-level properties that children can inherit.

The `SocialMedia` block always requires at least one child `SocialMediaItem`.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | `SocialMediaItem` |
| Repeatable | ✅ Yes |

Multiple `SocialMedia` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Columns | `columns` | Number | `1` | `1`, `2`, `3`, `4` |
| Show Title | `showTitle` | Boolean | `true` | `true`, `false` |
| Show Icon | `showIcon` | Boolean | `true` | `true`, `false` |
| Icon Position | `iconPosition` | Enum | `right` | `left`, `right` |
| Items Order | `itemsOrder` | Enum | `rtl` | `ltr`, `rtl` |
| Title Color | `titleColor` | Color | `#1A1A1A` | Valid Color |
| Icon Color | `iconColor` | Color | `""` (none) | Valid Color |
| Background Color | `backgroundColor` | Color | `""` (per-platform shade) | Valid Color |
| Border Color | `borderColor` | Color | `transparent` | Valid Color |
| Shape | `shape` | Enum | `rounded` | `sharp`, `slightlyRounded`, `rounded`, `pill` |

---

## Property Details

### `columns`

Controls how many items appear in each row of the grid.

| Field | Value |
|-------|-------|
| Type | Number |
| Required | ❌ No |
| Default | `1` |

Supported values: `1`, `2`, `3`, `4`.

> ⚠️ `columns` can only be `4` when either `showTitle` or `showIcon` is `false`. With both the title and the icon visible, four columns would overcrowd the grid, so the compiler rejects the combination.

---

### `showTitle`

Controls whether the platform label is displayed on each item.

| Field | Value |
|-------|-------|
| Type | Boolean |
| Required | ❌ No |
| Default | `true` |

---

### `showIcon`

Controls whether the platform brand icon is displayed on each item.

| Field | Value |
|-------|-------|
| Type | Boolean |
| Required | ❌ No |
| Default | `true` |

> ⚠️ `showTitle` and `showIcon` cannot both be `false` at the same time. Doing so results in a semantic validation error, because an item with neither a label nor an icon would be invisible.

---

### `iconPosition`

Controls the placement of the icon relative to the label.

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ❌ No |
| Default | `right` |

Supported values:

- `left` — icon before the label
- `right` — icon after the label

---

### `itemsOrder`

Controls the reading direction of the items.

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ❌ No |
| Default | `rtl` |

Supported values:

- `rtl` — right-to-left
- `ltr` — left-to-right

---

### `titleColor`

Defines the color of the item labels.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#1A1A1A` |

When omitted on a child item, the parent value is inherited. Otherwise the default is used.

---

### `iconColor`

Optionally forces a single color on the platform icons.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `""` (none) |

When set, every hex fill, stroke, and gradient stop in the platform icons is recolored to this value, so both flat and full-color icons (such as Instagram's gradient or TikTok's accent layers) are tinted to the requested color.

---

### `backgroundColor`

Defines the background color behind each item.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `""` (per-platform soft shade) |

When omitted, each item uses a soft shade of its platform's brand color by default.

---

### `borderColor`

Defines the border color around each item.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `transparent` |

---

### `shape`

Defines the overall shape of each item button.

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

The compiler performs the following semantic validations on the `SocialMedia` block:

- `columns` must be one of `1`, `2`, `3`, or `4`.
- `columns` can only be `4` when either `showTitle` or `showIcon` is `false`.
- `showTitle` and `showIcon` cannot both be `false`.
- The block must contain at least one `SocialMediaItem` child.
- Unknown or duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.
- Color properties must contain valid color values.

---

## Children

### SocialMediaItem

A `SocialMediaItem` renders a single clickable platform button inside the grid.

#### Hierarchy

| Property | Value |
|----------|-------|
| Parent | `SocialMedia` |
| Repeatable | ✅ Yes |

#### Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Platform | `platform` | Enum | `""` (required) | See Supported Platforms |
| Title | `title` | String | `""` (platform name) | Any valid string |
| URL | `url` | URL | `""` (required) | Valid URL |
| Title Color | `titleColor` | Color | `""` (inherited) | Valid Color |
| Icon Color | `iconColor` | Color | `""` (inherited) | Valid Color |
| Background Color | `backgroundColor` | Color | `""` (inherited) | Valid Color |
| Border Color | `borderColor` | Color | `""` (inherited) | Valid Color |

Item-level properties that are omitted inherit their value from the parent `SocialMedia` block, and fall back to the parent defaults if the parent does not define them.

#### Required Properties

The following properties are mandatory on every `SocialMediaItem`:

- `platform`
- `url`

Failure to provide either of these results in a semantic validation error.

#### Supported Platforms

The `platform` property accepts one of the following values:

| Value | Brand |
|-------|-------|
| `instagram` | Instagram |
| `telegram` | Telegram |
| `youtube` | YouTube |
| `tiktok` | TikTok |
| `x` | X |
| `linkedin` | LinkedIn |
| `github` | GitHub |
| `spotify` | Spotify |
| `twitch` | Twitch |
| `pinterest` | Pinterest |
| `facebook` | Facebook |
| `patreon` | Patreon |

#### Property Details

##### `platform`

Selects the brand of the item. The selected platform determines the official brand icon shown on the button and the default soft background shade.

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ✅ Yes |
| Default | none |

Failure to provide this property results in a semantic validation error.

---

##### `title`

Overrides the label shown on the button.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

When omitted, the canonical display name of the selected platform (for example `GitHub`) is used automatically.

---

##### `url`

The destination the button links to when clicked.

| Field | Value |
|-------|-------|
| Type | URL |
| Required | ✅ Yes |

Failure to provide this property results in a semantic validation error.

---

##### `titleColor`, `iconColor`, `backgroundColor`, `borderColor`

These visual properties behave like their `SocialMedia` counterparts but apply only to the individual item. When omitted, they inherit the parent block's value.

| Property | Type | Inherits |
|----------|------|----------|
| `titleColor` | Color | Parent `titleColor` |
| `iconColor` | Color | Parent `iconColor` |
| `backgroundColor` | Color | Parent `backgroundColor` |
| `borderColor` | Color | Parent `borderColor` |

---

## Rendering Behavior

The `SocialMedia` block is rendered as a responsive CSS grid containing the item buttons:

- The grid uses the number of columns specified by `columns`.
- The reading direction is set by `itemsOrder`.
- Each `SocialMediaItem` renders as an `<a>` anchor styled as a button.
- The official brand icon is shown when `showIcon` is `true`.
- The label (the item `title` or the platform name) is shown when `showTitle` is `true`.
- Visual defaults from the parent are applied when a child omits a property.
- When no item background is specified, a soft shade of the platform's brand color is used.

---

## Examples

### Minimal Example

```lkr
SocialMedia {

    SocialMediaItem { platform: github, url: "https://github.com/me" }
    SocialMediaItem { platform: telegram, url: "https://t.me/linkora" }

}
```

---

### Customized Example

```lkr
SocialMedia {

    columns: 3

    showTitle: false

    showIcon: true

    iconPosition: left

    itemsOrder: ltr

    titleColor: "#1F2937"

    iconColor: "#111111"

    backgroundColor: "#FFFFFF"

    borderColor: "#E5E7EB"

    shape: pill

    SocialMediaItem { platform: instagram, url: "https://instagram.com/me" }
    SocialMediaItem { platform: youtube, url: "https://youtube.com/@me" }
    SocialMediaItem { platform: linkedin, url: "https://www.linkedin.com/in/me" }

}
```

---

### Custom Item Title

```lkr
SocialMedia {
    SocialMediaItem { platform: patreon, title: "Support Me", url: "https://patreon.com/me" }
}
```

---

## Invalid Examples

Missing required `platform` property:

```lkr
SocialMedia {
    SocialMediaItem { url: "https://github.com/me" }
}
```

❌ Missing required property `platform`.

---

Missing required `url` property:

```lkr
SocialMedia {
    SocialMediaItem { platform: github }
}
```

❌ Missing required property `url`.

---

Unsupported platform value:

```lkr
SocialMedia {
    SocialMediaItem { platform: snapchat, url: "https://snapchat.com/me" }
}
```

❌ `snapchat` is not a valid value for `platform`.

---

Invalid `columns` value:

```lkr
SocialMedia {
    columns: 5
    SocialMediaItem { platform: github, url: "https://github.com/me" }
}
```

❌ `columns` must be one of 1, 2, 3, or 4.

---

Four columns with both the icon and the title visible:

```lkr
SocialMedia {
    columns: 4
    SocialMediaItem { platform: github, url: "https://github.com/me" }
}
```

❌ `columns` can only be 4 when either `showTitle` or `showIcon` is false.

---

No children:

```lkr
SocialMedia {
}
```

❌ The block must contain at least one `SocialMediaItem` child.

---

Both `showTitle` and `showIcon` disabled:

```lkr
SocialMedia {
    showTitle: false
    showIcon: false
    SocialMediaItem { platform: github, url: "https://github.com/me" }
}
```

❌ `showTitle` and `showIcon` cannot both be `false`.

---

## Notes

💡 The `SocialMedia` block commonly appears after the `Link` blocks to present social profiles in a compact, branded grid.

💡 Icons loaded from the official Simple Icons collection fill with their exact brand color by default; setting `iconColor` recolors every icon to the requested color, including full-color icons such as the Instagram gradient.
