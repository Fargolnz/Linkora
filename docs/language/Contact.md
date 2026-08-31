# 📞 Contact

## Description

The `Contact` block renders a responsive grid of contact-method buttons, each linking out to a phone number, email, SMS, or website.

It serves as a container for `ContactItem` children. Every child represents one contact method button featuring its own generic icon and, optionally, a short label. The grid adapts to the number of columns you specify and is fully customizable through container-level properties that children can inherit.

The `Contact` block always requires at least one child `ContactItem`.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | `ContactItem` |
| Repeatable | ✅ Yes |

Multiple `Contact` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Columns | `columns` | Number | `1` | `1`, `2`, `3`, `4` |
| Show Title | `showTitle` | Boolean | `true` | `true`, `false` |
| Show Icon | `showIcon` | Boolean | `true` | `true`, `false` |
| Icon Position | `iconPosition` | Enum | `right` | `left`, `right` |
| Items Order | `itemsOrder` | Enum | `rtl` | `ltr`, `rtl` |
| Title Color | `titleColor` | Color | `#00B4B0` | Valid Color |
| Icon Color | `iconColor` | Color | `#00B4B0` | Valid Color |
| Background Color | `backgroundColor` | Color | `#FFFFFF` | Valid Color |
| Border Color | `borderColor` | Color | `#00B4B0` | Valid Color |
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

Controls whether the contact method label is displayed on each item.

| Field | Value |
|-------|-------|
| Type | Boolean |
| Required | ❌ No |
| Default | `true` |

---

### `showIcon`

Controls whether the contact method icon is displayed on each item.

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
| Default | `#00B4B0` |

When omitted on a child item, the parent value is inherited. Otherwise the default is used.

---

### `iconColor`

Optionally forces a single color on the contact icons.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#00B4B0` |

When set, every hex fill, stroke, and gradient stop in the contact icons is recolored to this value.

---

### `backgroundColor`

Defines the background color behind each item.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#FFFFFF` |

---

### `borderColor`

Defines the border color around each item.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#00B4B0` |

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

The compiler performs the following semantic validations on the `Contact` block:

- `columns` must be one of `1`, `2`, `3`, or `4`.
- `columns` can only be `4` when either `showTitle` or `showIcon` is `false`.
- `showTitle` and `showIcon` cannot both be `false`.
- The block must contain at least one `ContactItem` child.
- Unknown or duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.
- Color properties must contain valid color values.

---

## Children

### ContactItem

A `ContactItem` renders a single clickable contact-method button inside the grid.

#### Hierarchy

| Property | Value |
|----------|-------|
| Parent | `Contact` |
| Repeatable | ✅ Yes |

#### Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Service | `service` | Enum | `""` (required) | See Supported Services |
| Title | `title` | String | `""` (service name) | Any valid string |
| Value | `value` | String | `""` (required) | Any valid string |
| Title Color | `titleColor` | Color | `""` (inherited) | Valid Color |
| Icon Color | `iconColor` | Color | `""` (inherited) | Valid Color |
| Background Color | `backgroundColor` | Color | `""` (inherited) | Valid Color |
| Border Color | `borderColor` | Color | `""` (inherited) | Valid Color |

Item-level properties that are omitted inherit their value from the parent `Contact` block, and fall back to the parent defaults if the parent does not define them.

#### Required Properties

The following properties are mandatory on every `ContactItem`:

- `service`
- `value`

Failure to provide either of these results in a semantic validation error.

#### Supported Services

The `service` property accepts one of the following values:

| Value | Name | URI Scheme |
|-------|------|-----------|
| `mobile` | Mobile | `tel:` |
| `phone` | Phone | `tel:` |
| `email` | Email | `mailto:` |
| `sms` | SMS | `sms:` |
| `website` | Website | `https://` |

#### Property Details

##### `service`

Selects the contact method of the item. The selected service determines the generic icon shown on the button and the URI scheme used to build the item's href.

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

When omitted, the canonical display name of the selected service (for example `Email`) is used automatically.

---

##### `value`

The raw contact value (phone number, email address, etc.) to link to. The rendered href is built by prepending the appropriate URI scheme for the item's `service`.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ✅ Yes |

Failure to provide this property results in a semantic validation error.

> 💡 For `website` items, if the value already contains `://`, no scheme is prepended.

---

##### `titleColor`, `iconColor`, `backgroundColor`, `borderColor`

These visual properties behave like their `Contact` counterparts but apply only to the individual item. When omitted, they inherit the parent block's value.

| Property | Type | Inherits |
|----------|------|----------|
| `titleColor` | Color | Parent `titleColor` |
| `iconColor` | Color | Parent `iconColor` |
| `backgroundColor` | Color | Parent `backgroundColor` |
| `borderColor` | Color | Parent `borderColor` |

---

## Rendering Behavior

The `Contact` block is rendered as a responsive CSS grid containing the item buttons:

- The grid uses the number of columns specified by `columns`.
- The reading direction is set by `itemsOrder`.
- Each `ContactItem` renders as an `<a>` anchor styled as a button.
- The generic icon is shown when `showIcon` is `true`.
- The label (the item `title` or the service name) is shown when `showTitle` is `true`.
- Visual defaults from the parent are applied when a child omits a property.
- Each item's href is built using the appropriate URI scheme for its `service`.

> 💡 `Contact` shares its visual styles with `SocialMedia` and `SocialNetwork`, so all three blocks render identical grids and buttons and can share styling.

---

## Examples

### Minimal Example

```lkr
Contact {

    ContactItem { service: mobile, value: "+1 234 567 8901" }
    ContactItem { service: email, value: "hi@example.com" }

}
```

---

### Customized Example

```lkr
Contact {

    columns: 2

    showTitle: false

    showIcon: true

    iconPosition: left

    itemsOrder: ltr

    titleColor: "#1F2937"

    iconColor: "#111111"

    backgroundColor: "#FFFFFF"

    borderColor: "#E5E7EB"

    shape: pill

    ContactItem { service: mobile, value: "+1 234 567 8901" }
    ContactItem { service: email, value: "hi@example.com" }
    ContactItem { service: website, value: "https://example.com" }

}
```

---

### Custom Item Title

```lkr
Contact {
    ContactItem { service: email, title: "Email Me", value: "hi@example.com" }
}
```

---

## Invalid Examples

Missing required `service` property:

```lkr
Contact {
    ContactItem { value: "hi@example.com" }
}
```

❌ Missing required property `service`.

---

Missing required `value` property:

```lkr
Contact {
    ContactItem { service: email }
}
```

❌ Missing required property `value`.

---

Invalid `columns` value:

```lkr
Contact {
    columns: 5
    ContactItem { service: mobile, value: "+1 234 567 8901" }
}
```

❌ `columns` must be one of 1, 2, 3, or 4.

---

Four columns with both the icon and the title visible:

```lkr
Contact {
    columns: 4
    ContactItem { service: mobile, value: "+1 234 567 8901" }
}
```

❌ `columns` can only be 4 when either `showTitle` or `showIcon` is false.

---

No children:

```lkr
Contact {
}
```

❌ The block must contain at least one `ContactItem` child.

---

Both `showTitle` and `showIcon` disabled:

```lkr
Contact {
    showTitle: false
    showIcon: false
    ContactItem { service: mobile, value: "+1 234 567 8901" }
}
```

❌ `showTitle` and `showIcon` cannot both be `false`.

---

## Notes

💡 The `Contact` block commonly appears to list contact methods (phone, email, website) in a compact, branded grid.

💡 Icons load with a generic brand color; setting `iconColor` recolors every icon to the requested color.
</content>
