# 📄 Page

## Description

The `Page` block describes the whole document rather than rendering content. It sets the page language, browser title, meta description, and favicon. Because the language is read from this block, it also drives the default direction of grid blocks and the default countdown label language across the entire page.

`Page` renders nothing inside the body — it only affects the `<head>` and the document defaults.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | None |
| Repeatable | ❌ No (at most one per document) |

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Language | `language` | Enum | `fa` | `fa`, `en` |
| Title | `title` | String | `""` | Any valid string |
| Description | `description` | String | `""` | Any valid string |
| Favicon | `favicon` | Image | `""` | Any valid image path/URL |

---

## Property Details

### `language`

Selects the page language and the defaults derived from it.

| Field | Value |
|-------|-------|
| Type | Enum |
| Required | ❌ No |
| Default | `fa` |

Supported values:

| Value | Description |
|-------|-------------|
| `fa` | Persian — the page is rendered as `lang="fa" dir="rtl"`, and grid blocks default to `direction: rtl` |
| `en` | English — the page is rendered as `lang="en" dir="ltr"`, grid blocks default to `direction: ltr`, and `Countdown` defaults to `language: en` |

The language only sets **defaults**. Any explicit block property, and any `Theme` block override, still wins over the page-derived value.

---

### `title`

Sets the `<title>` of the generated page. When omitted, the compiler falls back to `Linkora`.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

---

### `description`

Sets the `<meta name="description">` of the generated page. When omitted, no meta description is emitted.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ❌ No |
| Default | `""` |

---

### `favicon`

Sets the `<link rel="icon">` of the generated page. It can be a local file path or an external URL.

| Field | Value |
|-------|-------|
| Type | Image |
| Required | ❌ No |
| Default | `""` |

Local files referenced here are automatically copied into the output directory at compile time, exactly like images in `Image` and `Banner` blocks.

---

## Semantic Rules

The compiler performs the following semantic validations on the `Page` block:

- The block may appear at most once within the document.
- `language` must be `fa` or `en`.
- Unknown or duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.

---

## Rendering Behavior

The `Page` block contributes to the page shell but renders nothing in the body:

- `<html lang="{fa|en}" dir="{rtl|ltr}">` — the direction attribute reflects `language`.
- `<title>{title or "Linkora"}</title>`.
- `<meta name="description" content="...">` — only when `description` is set.
- `<link rel="icon" href="...">` — only when `favicon` is set.
- `language: en` also defaults `direction` to `ltr` for `SocialMedia`, `SocialNetwork`, `Contact`, `Address`, `FAQ`, `SuperLink`, `Image`, and `Banner`, and defaults each `Countdown` `language` to `en`.
- `language: fa` (or no `Page` block) keeps every block's existing `rtl` / `fa` defaults.

Explicit block properties and `Theme` overrides take precedence over these page-derived defaults.

---

## Examples

### Minimal Example

```lkr
Page {

    language: en

    title: "Fargol — Links"

}
```

With `language: en`, every grid block and countdown on this page defaults to English/`ltr` without setting them individually.

---

## Invalid Examples

More than one `Page` block:

```lkr
Page { language: fa }
Page { language: en }
```

❌ The `Page` block may appear only once.

---

Invalid `language` value:

```lkr
Page { language: de }
```

❌ `language` is not a valid value.

---

## Notes

💡 The `Page` block is optional. Documents without it compile to a Persian (`fa`, `rtl`) page titled `Linkora`, matching the current defaults.

💡 Precedence is: explicit block property > `Theme` override > `Page.language` default > schema default.

💡 There is no requirement to place `Page` first — block order in the document does not matter.