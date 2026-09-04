# 🎬 Video

## Description

The `Video` block renders a clickable video card with a thumbnail and a play icon overlay. It supports YouTube, Aparat, and local video files.

When the video source is **external** (YouTube or Aparat), the entire card links to the watch page and opens in a new tab. When the video source is **local** (`.mp4`, `.webm`, `.mov`), an inline `<video>` player with controls is rendered directly on the page.

For YouTube URLs, the thumbnail is auto-generated from the video ID. For Aparat and local videos, a play icon placeholder is shown if no custom thumbnail is provided.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Repeatable | ✅ Yes |

Multiple `Video` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Video URL | `url` | Video | `""` (required) | YouTube URL, Aparat URL, or local video file |
| Thumbnail | `thumbnail` | Image | `""` | Any valid image path/URL |
| Shape | `shape` | Enum | `rounded` | `sharp`, `slightlyRounded`, `rounded`, `pill` |
| Border Color | `borderColor` | Color | `transparent` | Valid Color |

---

## Property Details

### `url`

The video source URL. Accepts three types of URLs:

| Type | Example | Behavior |
|------|---------|----------|
| YouTube | `https://www.youtube.com/watch?v=abc123` | Links to watch page, auto-generates thumbnail |
| YouTube Short | `https://youtu.be/abc123` | Same as above |
| Aparat | `https://www.aparat.com/v/abc123` | Links to watch page, play icon placeholder |
| Local File | `./assets/intro.mp4` | Inline `<video>` player with controls |

Supported local video extensions: `.mp4`, `.webm`, `.mov`

| Field | Value |
|-------|-------|
| Type | Video |
| Required | ✅ Yes |

---

### `thumbnail`

A custom thumbnail image displayed over the video card with a play icon overlay.

| Field | Value |
|-------|-------|
| Type | Image |
| Required | ❌ No |
| Default | `""` |

Auto-generation behavior when omitted:

| Source | Thumbnail |
|--------|-----------|
| YouTube | Auto-generated from `img.youtube.com/vi/{ID}/maxresdefault.jpg` |
| Aparat | Play icon placeholder |
| Local | Play icon placeholder |

Local files referenced here are automatically copied into the output directory at compile time.

---

### `shape`

Defines the corner shape of the video card.

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

### `borderColor`

Defines the border color around the video card.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `transparent` |

---

## Semantic Rules

The compiler performs the following semantic validations on the `Video` block:

- `url` must be a valid YouTube URL, Aparat URL, or local video file path.
- `shape` must be one of the predefined enum values.
- `borderColor` must be a valid hex color or `transparent`.
- Unknown or duplicate properties are not allowed.

---

## Rendering Behavior

The `Video` block renders differently based on the video source:

### External Videos (YouTube / Aparat)

- The entire card is wrapped in an `<a>` tag linking to the video URL.
- Opens in a new tab (`target="_blank"`).
- Thumbnail is displayed with a static play icon overlay (white triangle in a dark circle).
- On hover (desktop), the card lifts slightly (`translateY(-2px)`) — a subtle visual cue that the card is interactive.

### Local Videos

- The card is wrapped in a `<div>` (not a link).
- A `<video>` element with `controls` and `preload="metadata"` is rendered.
- The thumbnail is shown as a poster image if provided.
- A static play icon overlay is always visible.

---

## Examples

### YouTube Example

```lkr
Video { url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ" }
```

---

### Aparat Example

```lkr
Video { url: "https://www.aparat.com/v/abc123" }
```

---

### Local Video with Custom Thumbnail

```lkr
Video {
    url: "./assets/intro.mp4"
    thumbnail: "./assets/intro-thumb.jpg"
    shape: slightlyRounded
}
```

---

### Customized Example

```lkr
Video {
    url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    thumbnail: "./assets/custom-thumb.jpg"
    shape: pill
    borderColor: "#333333"
}
```

---

## Invalid Examples

Missing required `url` property:

```lkr
Video {
    shape: rounded
}
```

❌ Missing required property `url`.

---

Invalid URL format:

```lkr
Video { url: "not-a-url" }
```

❌ Expected a YouTube URL, Aparat URL, or a relative file path with a video extension.

---

Invalid shape value:

```lkr
Video { url: "https://www.youtube.com/watch?v=abc123", shape: circle }
```

❌ `shape` must be one of `sharp`, `slightlyRounded`, `rounded`, `pill`.

---

## Notes

💡 YouTube thumbnails are auto-generated. No need to provide a custom thumbnail unless you want to override it.

💡 Aparat thumbnails are not predictable from the URL, so a play icon placeholder is shown by default. Provide a custom `thumbnail` for a richer look.

💡 Local videos play inline with browser-native controls. No external dependencies are needed.
