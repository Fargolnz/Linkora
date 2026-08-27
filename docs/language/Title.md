# 🔖 Title

## Description

The `Title` block renders a single heading that divides and labels sections of the page.

It is used to give names to groups of content that follow, such as a "My Links" heading above a set of `Link` blocks. This makes the page easier to read and organize.

The appearance of the heading is determined by its local properties.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | None |
| Repeatable | ✅ Yes |

Multiple `Title` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Title | `title` | String | `""` | Any valid string |
| Alignment | `align` | Enum | `center` | `left`, `center`, `right` |
| Title Color | `titleColor` | Color | `#000000` | Valid Color |

---

## Required Properties

According to the Linkora language specification:

> Any property whose default value is an empty string (`""`) is considered **required**.

Therefore, the following property is mandatory:

- `title`

Failure to provide this property results in a semantic validation error.

---

## Property Details

### `title`

Defines the text displayed as the heading.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ✅ Yes |

Example:

```lkr
title: "My Links"
```

---

### `align`

Controls the horizontal alignment of the heading text.

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

Defines the color of the heading text.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#000000` |

---

## Semantic Rules

The compiler performs the following semantic validations:

- `title` must be provided.
- Unknown properties are not allowed.
- Duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.
- Color properties must contain valid color values.
- The `Title` block cannot contain child blocks.

---

## Rendering Behavior

The `Title` block is rendered as an `<h2>` heading element.

Rendering engines should:

- Display the heading text using `title`.
- Apply the specified text color via an inline style.
- Apply the specified horizontal alignment via an inline style.
- Use default values for omitted optional properties.

---

## Examples

### Minimal Example

```lkr
Title {

    title: "My Links"

}
```

---

### Customized Example

```lkr
Title {

    title: "Connect With Me"

    align: left

    titleColor: "#c7006e"

}
```

---

### Compact Syntax

```lkr
Title { title: "My Links" }
```

---

## Invalid Examples

Missing required property:

```lkr
Title {

}
```

❌ Missing required property `title`.

---

Invalid enum value:

```lkr
align: justify
```

❌ `justify` is not a valid value for `align`.

---

## Notes

💡 `Title` is commonly used to give sections of the page a heading and may appear multiple times within the same document.

💡 When optional properties are omitted, their default values are automatically applied during semantic analysis.
