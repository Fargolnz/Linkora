# 🔗 Link

## Description

The `Link` block creates a clickable button that redirects users to an external webpage.

It is the primary navigation component of the Linkora language and is intended for linking to websites, portfolios, repositories, documents, and other online resources.

The appearance of the button is determined by its local properties or, when omitted, by the global theme defaults.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | Page |
| Allowed Children | None |
| Repeatable | ✅ Yes |

Multiple `Link` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Link Title | `title` | String | `""` | Any valid string |
| URL | `url` | URL | `""` | Valid HTTP/HTTPS URL |
| Alignment | `align` | Enum | `center` | `left`, `center`, `right` |
| Title Color | `titleColor` | Color | `#FFFFFF` | Valid Color |
| Background Color | `backgroundColor` | Color | `#00B4B0` | Valid Color |
| Border Color | `borderColor` | Color | `transparent` | Valid Color |
| Shape | `shape` | Enum | `rounded` | `sharp`, `slightlyRounded`, `rounded`, `pill` |

---

## Required Properties

According to the Linkora language specification:

> Any property whose default value is an empty string (`""`) is considered **required**.

Therefore, the following properties are mandatory:

- `title`
- `url`

Failure to provide either property results in a semantic validation error.

---

## Property Details

### `title`

Defines the text displayed inside the button.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ✅ Yes |

Example:

```lkr
title: "GitHub"
```

---

### `url`

Specifies the destination address opened when the button is clicked.

| Field | Value |
|-------|-------|
| Type | URL |
| Required | ✅ Yes |

Supported URL schemes in Linkora v1.0:

- `http://`
- `https://`

Example:

```lkr
url: "https://github.com"
```

---

### `align`

Controls the horizontal alignment of the button label.

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ❌ No |
| Default | `center` |

Supported values:

- `left`
- `center`
- `right`

---

### `titleColor`

Defines the color of the button text.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#FFFFFF` |

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

Defines the button border color.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `transparent` |

---

### `shape`

Defines the overall button shape.

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
| `pill` | Fully rounded pill-shaped button |

---

## Semantic Rules

The compiler performs the following semantic validations:

- `title` must be provided.
- `url` must be provided.
- `url` must be a valid HTTP or HTTPS URL.
- Unknown properties are not allowed.
- Duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.
- Color properties must contain valid color values.
- The `Link` block cannot contain child blocks.

---

## Rendering Behavior

The `Link` block is rendered as a clickable button.

Rendering engines should:

- Display the button label using `title`.
- Navigate to `url` when clicked.
- Apply the specified visual properties.
- Use default values for omitted optional properties.

---

## Examples

### Minimal Example

```lkr
Link {

    title: "GitHub"

    url: "https://github.com"

}
```

---

### Customized Example

```lkr
Link {

    title: "Portfolio"

    url: "https://example.com"

    align: left

    titleColor: "#FFFFFF"

    backgroundColor: "#3B82F6"

    borderColor: "#2563EB"

    shape: pill

}
```

---

### Compact Syntax

```lkr
Link { title: "GitHub", url: "https://github.com" }
```

---

## Invalid Examples

Missing required property:

```lkr
Link {

    title: "GitHub"

}
```

❌ Missing required property `url`.

---

Invalid enum value:

```lkr
shape: roundedLarge
```

❌ `roundedLarge` is not a valid value for `shape`.

---

Invalid URL:

```lkr
url: "github.com"
```

❌ URL must contain a valid supported scheme.

---

## Notes

💡 `Link` is one of the most commonly used blocks in Linkora and may appear multiple times within the same document.

💡 When optional properties are omitted, their default values are automatically applied during semantic analysis.