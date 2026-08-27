# 👤 Profile

## Description

The `Profile` block is the identity section at the top of every Linkora page.

It serves as a container for the user's personal information — display name, profile image, biography, and cover banner. All child blocks render inside a centered vertical layout with consistent spacing.

Every child of `Profile` is optional, allowing users to include only the elements they need.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | `Name`, `Logo`, `Bio`, `Cover` |
| Repeatable | ❌ No |

The `Profile` block is a top-level block and may appear at most once per document.

---

## Properties

The `Profile` block does not define any configurable properties.

Its behavior is determined entirely by its children.

---

## Required Properties

Some child blocks define configurable properties that are **required**:

| Child | Required Property |
|-------|-------------------|
| `Name` | `title` |
| `Logo` | `image` |
| `Bio` | `text` |
| `Cover` | `image` |

Failure to provide a required property results in a semantic validation error.

---

## Children

Children may appear in any order inside the `Profile` block. The renderer automatically sorts them into the correct display order: **Cover → Logo → Name → Bio**.

| Child | Description | Required | Repeatable |
|-------|-------------|----------|------------|
| `Name` | Display name and subtitle | ❌ No | ❌ No |
| `Logo` | Profile image | ❌ No | ❌ No |
| `Bio` | Biography text | ❌ No | ❌ No |
| `Cover` | Cover/banner image | ❌ No | ❌ No |

---

### 🪪 Name

Displays the user's identity — main title and subtitle.

#### Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Title | `title` | String | `""` | Any valid string |
| Subtitle | `subtitle` | String | `""` | Any valid string |
| Text Alignment | `align` | Enum | `center` | `left`, `center`, `right` |
| Title Color | `titleColor` | Color | `#000000` | Valid Color |
| Subtitle Color | `subColor` | Color | `#000000` | Valid Color |

#### Rendering

- `title` renders as an `<h1>` element.
- `subtitle` renders as a `<p>` element below the title.
- Both elements are hidden when their value is empty.
- Text alignment is applied via inline `text-align` style.

#### Example

```lkr
Name {
    title: "Seyyedeh Fargol Nazemzadeh"
    subtitle: "Developer & Designer"
    align: center
    titleColor: "#000000"
    subColor: "#666666"
}
```

---

### 📝 Bio

Displays a short biography or description.

#### Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Bio Text | `text` | String | `""` | Any valid string |
| Text Alignment | `align` | Enum | `center` | `left`, `center`, `right` |
| Text Color | `textColor` | Color | `#000000` | Valid Color |
| Background Color | `backgroundColor` | Color | `transparent` | Valid Color |
| Border Color | `borderColor` | Color | `transparent` | Valid Color |
| Shape | `shape` | Enum | `rounded` | `sharp`, `slightlyRounded`, `rounded`, `pill` |

#### Rendering

- Renders as a `<p>` element with full width.
- Text alignment is applied via inline `text-align` style.
- Border and background are applied when non-transparent.

#### Example

```lkr
Bio {
    text: "Building Linkora — a DSL for customizable link-in-bio pages."
    align: left
    textColor: "#333333"
    shape: rounded
}
```

---

### 🖼️ Logo

Displays the user's profile image.

#### Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Image | `image` | Image | `""` | Image URL or local path |
| Shape | `shape` | Enum | `circle` | `circle`, `square` |
| Border Color | `borderColor` | Color | `transparent` | Valid Color |

#### Image Support

The `image` property accepts:

- **URL**: `https://example.com/photo.jpg`
- **Local path**: `./assets/logo.png`

Supported formats: `.jpg`, `.jpeg`, `.png`, `.svg`, `.gif`, `.webp`

Local files are automatically copied to the output directory during compilation.

#### Rendering

- Renders as a 96×96 `<img>` element.
- `circle` shape applies `border-radius: 50%`.
- `square` shape applies no border radius.
- Border is rendered as a 3px solid border.

#### Example

```lkr
Logo {
    image: "./assets/profile.jpg"
    shape: square
    borderColor: "#00B4B0"
}
```

---

### 🎨 Cover

Displays a cover/banner image above the profile information.

#### Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Image | `image` | Image | `""` | Image URL or local path |
| Shape | `shape` | Enum | `rounded` | `rectangle`, `rounded` |

#### Image Support

The `image` property accepts:

- **URL**: `https://example.com/cover.jpg`
- **Local path**: `./assets/cover.jpg`

Supported formats: `.jpg`, `.jpeg`, `.png`, `.svg`, `.gif`, `.webp`

Local files are automatically copied to the output directory during compilation.

#### Rendering

- Renders as a full-width `<div>` containing an `<img>` element.
- Image height is fixed at 160px with `object-fit: cover`.
- `rounded` shape applies `border-radius: 16px` to the image.
- `rectangle` shape applies no border radius.
- The cover extends edge-to-edge horizontally, overriding page padding.

#### Example

```lkr
Cover {
    image: "./assets/banner.jpg"
    shape: rounded
}
```

---

## Semantic Rules

The compiler performs the following semantic validations:

- The `Profile` block may appear at most once per document.
- Children must be valid child block types (`Name`, `Logo`, `Bio`, `Cover`).
- Each child type may appear at most once inside `Profile`.
- Required properties must be provided (`Name.title`, `Logo.image`, `Bio.text`, `Cover.image`).
- `image` properties in `Logo` and `Cover` must be valid image URLs or local paths with supported extensions.
- Unknown properties are not allowed inside any child block.
- Duplicate properties are not allowed inside any child block.
- Enum properties must contain one of their predefined values.
- Color properties must contain valid color values.

---

## Rendering Behavior

The `Profile` block is rendered as a `<section>` element with a centered vertical layout.

Rendering engines should:

1. Sort children into display order: Cover → Logo → Name → Bio.
2. Render each child inside the Profile section.
3. Apply consistent spacing between children (16px gap).
4. Add bottom padding to separate Profile from subsequent content.

---

## Examples

### Minimal Example

```lkr
Profile {
    Name { title: "Fargol" }
}
```

---

### Full Example

```lkr
Profile {
    Cover { image: "./assets/cover.jpg", shape: rounded }
    Logo { image: "./assets/photo.jpg", shape: circle }
    Name {
        title: "Seyyedeh Fargol Nazemzadeh"
        subtitle: "Developer & Designer"
        titleColor: "#000000"
        subColor: "#666666"
    }
    Bio {
        text: "Building Linkora — a DSL for customizable link-in-bio pages."
        align: center
        textColor: "#333333"
    }
}
```

---

### Compact Syntax

```lkr
Profile { Name { title: "Jane" } Logo { image: "https://x.com/photo.jpg" } }
```

---

## Invalid Examples

Multiple Profile blocks:

```lkr
Profile { Name { title: "A" } }
Profile { Name { title: "B" } }
```

❌ A Linkora document may contain only one `Profile` block.

---

Invalid child block:

```lkr
Profile {
    Link { title: "GitHub", url: "https://github.com" }
}
```

❌ `Link` is not a valid child of `Profile`. Only `Name`, `Logo`, `Bio`, and `Cover` are allowed.

---

Invalid image path:

```lkr
Logo { image: "./assets/photo.txt" }
```

❌ Image must have a supported extension (`.jpg`, `.jpeg`, `.png`, `.svg`, `.gif`, `.webp`).

---

## Notes

💡 The `Profile` block is always rendered first on the page, before any other top-level blocks.

💡 Children can be written in any order — the renderer sorts them automatically.

💡 All children are optional. A `Profile` block with no children renders as an empty section.

💡 Local image files are copied to the `assets/` directory in the output folder during compilation.
