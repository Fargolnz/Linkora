# 🎨 Theme

## Description

The `Theme` block styles the whole page from a single place. It never renders
its own markup — instead its values become the *defaults* used for any optional
block property the author left unset, so every card on the page shares one
consistent look.

There are two ways the `Theme` block affects the page:

1. `primaryColor` becomes the accent color used everywhere a block's default is
   an accent (for example `Link.backgroundColor`, `Divider.color`, the FAQ
   question, and the contact icons/borders).
2. Its child blocks (`LinkTheme`, `GridTheme`, …) provide per-block defaults:
   any property you write there is applied to every matching block that does not
   set that property itself.

A page can contain **at most one** `Theme` block, and blocks that do not exist
(`BoxTheme`…) or that escape the `Theme` container produce errors.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | `PageTheme`, `LinkTheme`, `SuperLinkTheme`, `GridTheme`, `TitleTheme`, `ImageTheme`, `BannerTheme`, `DividerTheme`, `VideoTheme` |
| Repeatable | ❌ No |

Once per page, at the top level.

---

## Priority

When a property's final value is computed, the most specific value wins:

1. The block's own explicit property.
2. The matching `*Theme` child's property (or `primaryColor`).
3. The built-in default from the schema.

```lkr
Theme {
    primaryColor: "#C7006E"
    LinkTheme { shape: pill }
}

Link { title: "One", url: "https://example.com" }
Link { title: "Two", url: "https://example.com", shape: sharp }
```

`One` becomes a pill (`#C7006E`) using the theme. `Two` pins `shape: sharp`, and
the theme is only its `backgroundColor` default.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Primary Color | `primaryColor` | Color | *(unset)* | Valid opaque Color |

---

### `primaryColor`

Defines the page's accent color. It is used as the default value for the
highlighted properties of the blocks listed below — when those blocks don't set
the property themselves:

| Identifiers | Property |
|-------------|----------|
| `Link`, `SuperLink` | `backgroundColor` |
| `Divider` | `color` |
| `Contact` | `iconColor`, `borderColor`, `titleColor` |
| `Countdown` | `textColor` |
| `FAQ` | `questionColor`, `iconColor`, `borderColor` |

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | *(unset — schema defaults are used)* |

---

## Semantic Rules

The compiler performs the following checks on the `Theme` block:

- The `Theme` block is not repeatable.
- Unknown or duplicate properties are not allowed.
- `primaryColor` must be a valid opaque color.
- Only the documented child blocks are allowed inside `Theme`, and each may
  appear at most once.
- The `*Theme` child blocks may not appear anywhere else in the document.

---

## Child Blocks

### `PageTheme`

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Font Family | `fontFamily` | Enum | *(unset)* | `vazirmatn`, `inter`, `poppins`, `rubik`, `roboto` |
| Background Color | `backgroundColor` | Color | *(unset — `#ffffff`)* | Valid opaque Color |
| Backdrop Color | `backdropColor` | Color | *(unset — `#e0f4f4`)* | Valid Color or `transparent` |
| Background Image | `backgroundImage` | Image | *(unset — `none`)* | Valid `Image` |
| Background Size | `backgroundSize` | Enum | *(unset — `cover`)* | `cover`, `contain`, `auto` |
| Background Repeat | `backgroundRepeat` | Enum | *(unset — `noRepeat`)* | `repeat`, `noRepeat`, `repeatX`, `repeatY` |

The page background and font. `backgroundColor` must be opaque (a *transparent*
page would make the backdrop show through); `backdropColor` may be
`transparent` to drop the desktop card backdrop.

`backgroundImage` paints an image behind the page content; when it is
*(unset)* or `none`, no image is drawn and the plain `backgroundColor`
shows instead.

`backgroundSize` controls how the image is scaled:
`cover` fills the whole page (cropping if needed), `contain` fits the
whole image inside it, and `auto` keeps its natural size.

`backgroundRepeat` decides whether the image tiles: `repeat` tiles both
ways, `noRepeat` shows it once, and `repeatX`/`repeatY` tile along one
axis only. `repeatX`/`repeatY` are most useful with a small image whose
size is left `auto`.

> Note that `backgroundRepeat` only has a visible effect when the image is
smaller than the page. With the default `backgroundSize: cover`, the image
is scaled to fill the whole page (cropping as needed), so it never has any
room to tile and the repeat never shows. To actually see
`repeat`/`repeatX`/`repeatY`, set `backgroundSize` to `contain` or `auto`
first so there is empty space left over for the image to tile into.

---

### `TitleTheme`

| Property | Keyword | Type | Default |
|----------|---------|------|---------|
| Title Color | `titleColor` | Color | *(inherited)* |
| Align | `align` | Enum | `left`, `center`, `right` |

Applies to every `Title` block.

---

### `LinkTheme`

| Property | Keyword | Type | Default |
|----------|---------|------|---------|
| Title Color | `titleColor` | Color | *(inherited)* |
| Background Color | `backgroundColor` | Color | *(inherited)* |
| Border Color | `borderColor` | Color | *(inherited)* |
| Shape | `shape` | Enum | `sharp`, `slightlyRounded`, `rounded`, `pill` |

Applies to every `Link` block.

---

### `SuperLinkTheme`

| Property | Keyword | Type | Default |
|----------|---------|------|---------|
| Title Color | `titleColor` | Color | *(inherited)* |
| Description Color | `descriptionColor` | Color | *(inherited)* |
| Icon Color | `iconColor` | Color | *(inherited)* |
| Background Color | `backgroundColor` | Color | *(inherited)* |
| Border Color | `borderColor` | Color | *(inherited)* |
| Shape | `shape` | Enum | `sharp`, `slightlyRounded`, `rounded`, `pill` |

Applies to every `SuperLink` block.

---

### `GridTheme`

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Columns | `columns` | Number | *(inherited)* | 1, 2, 3, 4 |
| Show Title | `showTitle` | Boolean | *(inherited)* | `true`, `false` |
| Show Icon | `showIcon` | Boolean | *(inherited)* | `true`, `false` |
| Direction | `direction` | Enum | *(inherited)* | `ltr`, `rtl` |
| Title Color | `titleColor` | Color | *(inherited)* | |
| Icon Color | `iconColor` | Color | *(inherited)* | |
| Background Color | `backgroundColor` | Color | *(inherited)* | |
| Border Color | `borderColor` | Color | *(inherited)* | |
| Shape | `shape` | Enum | `sharp`, `slightlyRounded`, `rounded`, `pill` |

Applies to the `SocialMedia`, `SocialNetwork`, `Contact`, and `Address` grids
with the same cross-field rules as those blocks: `'showTitle'` and `'showIcon'`
cannot both be `false`, and `columns` may only be 4 when one of them is `false`.

---

### `ImageTheme`

| Property | Keyword | Type | Default |
|----------|---------|------|---------|
| Shape | `shape` | Enum | `sharp`, `slightlyRounded`, `rounded` |
| Title Color | `titleColor` | Color | *(inherited)* |
| Description Color | `descriptionColor` | Color | *(inherited)* |
| Background Color | `backgroundColor` | Color | *(inherited)* |
| Border Color | `borderColor` | Color | *(inherited)* |
| Image Shadow | `shadow` | Boolean | *(inherited)* |

Applies to every `Image` block.

---

### `BannerTheme`

| Property | Keyword | Type | Default |
|----------|---------|------|---------|
| Shape | `shape` | Enum | `sharp`, `slightlyRounded`, `rounded` |
| Title Color | `titleColor` | Color | *(inherited)* |
| Description Color | `descriptionColor` | Color | *(inherited)* |
| Border Color | `borderColor` | Color | *(inherited)* |

Applies to every `Banner` block.

---

### `VideoTheme`

| Property | Keyword | Type | Default |
|----------|---------|------|---------|
| Shape | `shape` | Enum | `sharp`, `slightlyRounded`, `rounded` |
| Border Color | `borderColor` | Color | *(inherited)* |

Applies to every `Video` block.

---

### `DividerTheme`

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Color | `color` | Color | *(inherited)* | Valid Color |
| Margin Top | `marginTop` | Number | *(inherited)* | Integer 8 – 200 |
| Margin Bottom | `marginBottom` | Number | *(inherited)* | Integer 8 – 200 |

Applies to every `Divider` block, with the same 8–200 margin limits as the
`Divider` block itself.

---

## Examples

### Minimal Example

```lkr
Theme {
    primaryColor: "#C7006E"
}
```

Recolors every accent-colored default across the page.

### Full Theme

```lkr
Theme {
    primaryColor: "#0EA5E9"
    PageTheme {
        backgroundColor: "#0F172A"
        backdropColor: transparent
        fontFamily: inter
    }
    LinkTheme { shape: pill }
    GridTheme { columns: 4, showTitle: false, showIcon: true }
    TitleTheme { titleColor: "#F8FAFC" }
    DividerTheme { marginTop: 48, marginBottom: 48, color: "#0EA5E9" }
}
```

A dark, blue-accented page: all links become pills filled with the accent, the
social grids collapse to 4 icon-only columns, headings become near-white, and
every divider gets wide margins in the accent color.

### Precedence Example

```lkr
Theme {
    LinkTheme { backgroundColor: "#111111" }
}

Link { title: "Theme colored", url: "https://example.com" }
Link { title: "Self colored", url: "https://example.com", backgroundColor: "#C7006E" }
```

The first link uses the dark theme background; the second keeps its own custom
background.

---

## Invalid Examples

Two theme blocks on one page:

```lkr
Theme { }
Theme { }
```

❌ The `Theme` block may appear only once.

A theme child outside the `Theme` block:

```lkr
LinkTheme { shape: pill }
```

❌ `LinkTheme` is only allowed inside the `Theme` block.

---

## Notes

💡 The `Theme` block renders no HTML of its own — it is a pure configuration block.

💡 Theme values act as *defaults* only: a block's own explicit property always
wins, so themes never fight per-block customization.

💡 `primaryColor` is expected to be opaque; a transparent page background would
make the backdrop leak through, so `PageTheme.backgroundColor` explicitly
rejects `transparent`.