# 📍 Address

## Description

The `Address` block renders an optional address caption together with a responsive grid of navigation buttons, each opening a route or location in a map provider.

It serves as a container for `AddressItem` children. Every child represents one map-provider button (Google Maps, Waze, Neshan, or Balad) featuring its official brand icon and, optionally, a short label. The grid adapts to the number of columns you specify and is fully customizable through container-level properties that children can inherit.

The `Address` block always requires at least one child `AddressItem`.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | `AddressItem` |
| Repeatable | ✅ Yes |

Multiple `Address` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Address | `address` | String | `""` | Any valid string |
| Address Color | `addressColor` | Color | `#000000` | Valid Color |
| Columns | `columns` | Number | `1` | `1`, `2`, `3`, `4` |
| Show Title | `showTitle` | Boolean | `true` | `true`, `false` |
| Show Icon | `showIcon` | Boolean | `true` | `true`, `false` |
| Icon Position | `iconPosition` | Enum | `right` | `left`, `right` |
| Items Order | `itemsOrder` | Enum | `rtl` | `ltr`, `rtl` |
| Title Color | `titleColor` | Color | `#3B3B3B` | Valid Color |
| Icon Color | `iconColor` | Color | `""` (brand color) | Valid Color |
| Background Color | `backgroundColor` | Color | per-service shade | Valid Color |
| Border Color | `borderColor` | Color | `transparent` | Valid Color |
| Shape | `shape` | Enum | `rounded` | `sharp`, `slightlyRounded`, `rounded`, `pill` |

---

## Property Details

### `address`

An optional string displayed as a caption above the grid, typically the street address of the location being linked to.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

When omitted (or empty), no caption is rendered.

---

### `addressColor`

Defines the color of the `address` caption text.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#000000` |

---

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

Controls whether the provider label is displayed on each item.

| Field | Value |
|-------|-------|
| Type | Boolean |
| Required | ❌ No |
| Default | `true` |

---

### `showIcon`

Controls whether the provider brand icon is displayed on each item.

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
| Default | `#3B3B3B` |

When omitted on a child item, the parent value is inherited. Otherwise the default is used.

---

### `iconColor`

Optionally forces a single color on the provider icons.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `""` |

When omitted, each provider renders its original full-color brand icon. When set, every hex fill, stroke, and gradient stop in the icons is recolored to this value.

---

### `backgroundColor`

Defines the background color behind each item.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | per-service shade |

When omitted on an item, a soft shade of the selected provider's brand color is used. When omitted on the container, the default applies to its children.

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

The compiler performs the following semantic validations on the `Address` block:

- `columns` must be one of `1`, `2`, `3`, or `4`.
- `columns` can only be `4` when either `showTitle` or `showIcon` is `false`.
- `showTitle` and `showIcon` cannot both be `false`.
- The block must contain at least one `AddressItem` child.
- Unknown or duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.
- Color properties must contain valid color values.

---

## Children

### AddressItem

An `AddressItem` renders a single clickable navigation button inside the grid.

#### Hierarchy

| Property | Value |
|----------|-------|
| Parent | `Address` |
| Repeatable | ✅ Yes |

#### Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Service | `service` | Enum | `""` (required) | See Supported Services |
| Title | `title` | String | `""` (service name) | Any valid string |
| URL | `url` | URL | `""` (required) | Any valid URL |
| Title Color | `titleColor` | Color | `""` (inherited) | Valid Color |
| Icon Color | `iconColor` | Color | `""` (inherited) | Valid Color |
| Background Color | `backgroundColor` | Color | `""` (inherited) | Valid Color |
| Border Color | `borderColor` | Color | `""` (inherited) | Valid Color |

Item-level properties that are omitted inherit their value from the parent `Address` block, and fall back to the parent defaults if the parent does not define them.

#### Required Properties

The following properties are mandatory on every `AddressItem`:

- `service`
- `url`

Failure to provide either of these results in a semantic validation error.

#### Supported Services

The `service` property accepts one of the following values:

| Value | Name |
|-------|------|
| `googleMap` | Google Maps |
| `waze` | Waze |
| `neshan` | Neshan |
| `balad` | Balad |

#### Property Details

##### `service`

Selects the map provider of the item. The selected service determines the brand icon shown on the button and the default soft background shade.

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

When omitted, the canonical display name of the selected service (for example `Google Maps`) is used automatically.

---

##### `url`

The full navigation URL to open in the selected provider. Unlike `value`-based blocks, the address is not auto-built: the `url` is used verbatim as the item's `href`.

| Field | Value |
|-------|-------|
| Type | URL |
| Required | ✅ Yes |

Failure to provide this property results in a semantic validation error.

---

##### `titleColor`, `iconColor`, `backgroundColor`, `borderColor`

These visual properties behave like their `Address` counterparts but apply only to the individual item. When omitted, they inherit the parent block's value.

| Property | Type | Inherits |
|----------|------|----------|
| `titleColor` | Color | Parent `titleColor` |
| `iconColor` | Color | Parent `iconColor` |
| `backgroundColor` | Color | Parent `backgroundColor` |
| `borderColor` | Color | Parent `borderColor` |

---

## Rendering Behavior

The `Address` block is rendered as an optional caption followed by a responsive CSS grid containing the item buttons:

- The `address` caption, when present, is shown above the grid in `addressColor`.
- The grid uses the number of columns specified by `columns`.
- The reading direction is set by `itemsOrder`.
- Each `AddressItem` renders as an `<a>` anchor styled as a button.
- The brand icon is shown when `showIcon` is `true`.
- The label (the item `title` or the service name) is shown when `showTitle` is `true`.
- Visual defaults from the parent are applied when a child omits a property.
- Each item's `href` is the item's `url` used verbatim.

> 💡 `Address` shares its visual styles with `SocialMedia`, `SocialNetwork`, and `Contact`, so all four blocks render identical grids and buttons and can share styling.

---

## Examples

### Minimal Example

```lkr
Address {

    AddressItem { service: googleMap, url: "https://maps.google.com/?q=Tehran" }
    AddressItem { service: waze, url: "https://waze.com/ul?q=Tehran" }

}
```

---

### Customized Example

```lkr
Address {

    columns: 2

    address: "Tehran, Iran"

    addressColor: "#111111"

    showTitle: true

    iconPosition: left

    itemsOrder: ltr

    titleColor: "#1F2937"

    iconColor: "#111111"

    backgroundColor: "#F3F4F6"

    borderColor: "#E5E7EB"

    shape: pill

    AddressItem { service: googleMap, url: "https://maps.google.com/?q=Tehran" }
    AddressItem { service: neshan, url: "https://neshan.org/maps/@35.689,51.389" }
    AddressItem { service: balad, url: "https://balad.ir/place?q=Tehran" }

}
```

---

### Custom Item Title

```lkr
Address {
    AddressItem { service: waze, title: "Open in Waze", url: "https://waze.com/ul?q=Tehran" }
}
```

---

## Invalid Examples

Missing required `service` property:

```lkr
Address {
    AddressItem { url: "https://maps.google.com/?q=Tehran" }
}
```

❌ Missing required property `service`.

---

Missing required `url` property:

```lkr
Address {
    AddressItem { service: googleMap }
}
```

❌ Missing required property `url`.

---

Invalid `columns` value:

```lkr
Address {
    columns: 5
    AddressItem { service: googleMap, url: "https://maps.google.com/?q=Tehran" }
}
```

❌ `columns` must be one of 1, 2, 3, or 4.

---

Four columns with both the icon and the title visible:

```lkr
Address {
    columns: 4
    AddressItem { service: googleMap, url: "https://maps.google.com/?q=Tehran" }
}
```

❌ `columns` can only be 4 when either `showTitle` or `showIcon` is false.

---

No children:

```lkr
Address {
}
```

❌ The block must contain at least one `AddressItem` child.

---

Both `showTitle` and `showIcon` disabled:

```lkr
Address {
    showTitle: false
    showIcon: false
    AddressItem { service: googleMap, url: "https://maps.google.com/?q=Tehran" }
}
```

❌ `showTitle` and `showIcon` cannot both be `false`.

---

## Notes

💡 The `Address` block commonly appears to present a location and let visitors open it in their preferred map application.

💡 Icons load with their original brand colors; setting `iconColor` recolors every icon to the requested color.

💡 The `url` is used verbatim, so you should provide the full navigation link for the chosen provider.
