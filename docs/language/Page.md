# 📄 Page

## Description

The `Page` block is the root container of every Linkora document.

It defines the beginning and end of a page and serves as the parent container for all top-level content blocks.

Every valid Linkora source file must contain exactly one `Page` block.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | All top-level blocks |
| Repeatable | ❌ No |

The `Page` block is the only block that has no parent.

---

## Properties

The `Page` block does not define any configurable properties in Linkora v1.0.

Its sole purpose is to act as the root container for the page content.

---

## Semantic Rules

The compiler performs the following semantic validations:

- Exactly one `Page` block must exist in every document.
- The `Page` block must be the root block of the document.
- No blocks may exist outside the `Page` block.
- The `Page` block may only contain valid top-level blocks.
- Child blocks that belong to other parent blocks (such as `Name` inside `Profile`) cannot appear directly inside `Page`.

---

## Allowed Children

The following blocks may appear directly inside the `Page` block.

| Block |
|-------|
| `Theme` |
| `Profile` |
| `Title`|
| `Link` |
| `SuperLink` |
| `Text` |
| `Image` |
| `Banner` |
| `Video `|
| `SocialMedia` |
| `SocialNetwork` |
| `Contact` |
| `Address` |
| `FAQ` |
| `RSS` |
| `Countdown` |
| `Divider` |

> ℹ️ This list represents the Linkora v1.0 standard library and may be extended in future versions.

---

## Rendering Behavior

The `Page` block is not rendered as a visible UI component.

Instead, it defines the root container of the generated page.

During HTML generation, all child blocks are rendered sequentially inside the page container.

---

## Examples

### Minimal Example

```lkr
Page {

}
```

---

### Example with Child Blocks

```lkr
Page {

    Profile {

        Name {

            title: "Fargol"

        }

    }

    Link {

        title: "GitHub"

        url: "https://github.com"

    }

}
```

---

## Invalid Examples

Multiple root pages:

```lkr
Page {

}

Page {

}
```

❌ A Linkora document may contain only one `Page` block.

---

Blocks outside `Page`:

```lkr
Link {

    title: "GitHub"

    url: "https://github.com"

}
```

❌ All top-level blocks must be placed inside a `Page` block.

---

Invalid child block:

```lkr
Page {

    Name {

        title: "Fargol"

    }

}
```

❌ `Name` cannot appear directly inside `Page`.

---

## Notes

💡 Every Linkora document begins with a single `Page` block.

💡 The `Page` block acts as the root node of the Abstract Syntax Tree (AST).

💡 Although the `Page` block is not rendered directly, it determines the overall structure of the generated page.