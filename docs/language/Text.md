# 📝 Text

## Description

The `Text` block renders a standalone block of prose on the page.

It is used for longer, free-form paragraphs that do not belong to the profile section, such as an introduction, a description, or a closing note between groups of blocks.

The appearance of the text is determined by its local properties.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | None |
| Repeatable | ✅ Yes |

Multiple `Text` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Text | `text` | String | `""` | Any valid string |
| Alignment | `align` | Enum | `center` | `left`, `center`, `right` |
| Text Color | `textColor` | Color | `#000000` | Valid Color |
| Background Color | `backgroundColor` | Color | `transparent` | Valid Color |
| Border Color | `borderColor` | Color | `transparent` | Valid Color |
| Shape | `shape` | Enum | `rounded` | `sharp`, `slightlyRounded`, `rounded`, `pill` |

---

## Required Properties

According to the Linkora language specification:

> Any property whose default value is an empty string (`""`) is considered **required**.

Therefore, the following property is mandatory:

- `text`

Failure to provide this property results in a semantic validation error.

---

## Property Details

### `text`

Defines the prose displayed as the paragraph.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ✅ Yes |

Example:

```lkr
text: "A short introduction about me."
```

---

### `align`

Controls the horizontal alignment of the paragraph text.

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

### `textColor`

Defines the color of the paragraph text.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#000000` |

---

### `backgroundColor`

Defines the background color behind the paragraph.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `transparent` |

---

### `borderColor`

Defines the border color around the paragraph.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `transparent` |

---

### `shape`

Defines the overall shape of the paragraph box.

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

The compiler performs the following semantic validations:

- `text` must be provided.
- Unknown properties are not allowed.
- Duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.
- Color properties must contain valid color values.
- The `Text` block cannot contain child blocks.

---

## Rendering Behavior

The `Text` block is rendered as a `<p>` paragraph element.

Rendering engines should:

- Display the paragraph text using `text`.
- Apply the specified text color via an inline style.
- Apply the specified horizontal alignment via an inline style.
- Apply the background and border colors when they are not transparent.
- Apply the specified shape via a corner radius.
- Use default values for omitted optional properties.

---

## Examples

### Minimal Example

```lkr
Text {

    text: "A short introduction about me."

}
```

---

### Customized Example

```lkr
Text {

    text: "Welcome to my page!"

    align: left

    textColor: "#333333"

    backgroundColor: "#F3F4F6"

    borderColor: "#2563EB"

    shape: rounded

}
```

---

### Compact Syntax

```lkr
Text { text: "Welcome to my page!" }
```

---

## Invalid Examples

Missing required property:

```lkr
Text {

}
```

❌ Missing required property `text`.

---

Invalid enum value:

```lkr
shape: squircle
```

❌ `squircle` is not a valid value for `shape`.

---

## Notes

💡 The `Text` block is commonly used to give the page longer paragraphs and may appear multiple times within the same document.

💡 When optional properties are omitted, their default values are automatically applied during semantic analysis.
