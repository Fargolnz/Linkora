# ❓ FAQ

## Description

The `FAQ` block renders a set of expandable question-and-answer items. Visitors can click a question to reveal or hide its answer. Multiple items can be open at the same time.

It serves as a container for `FAQItem` children. Every child represents one question-and-answer pair with an expandable chevron icon. The container defines the default visual styling that each item inherits unless overridden.

The `FAQ` block always requires at least one child `FAQItem`.

---

## Hierarchy

| Property | Value |
|----------|-------|
| Parent | None |
| Allowed Children | `FAQItem` |
| Repeatable | ✅ Yes |

Multiple `FAQ` blocks may appear within the same document.

---

## Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Question Color | `questionColor` | Color | `#00B4B0` | Valid Color |
| Answer Color | `answerColor` | Color | `#3B3B3B` | Valid Color |
| Icon Color | `iconColor` | Color | `#00B4B0` | Valid Color |
| Background Color | `backgroundColor` | Color | `#FFFFFF` | Valid Color |
| Border Color | `borderColor` | Color | `#00B4B0` | Valid Color |
| Shape | `shape` | Enum | `rounded` | `sharp`, `slightlyRounded`, `rounded`, `pill` |

---

## Property Details

### `questionColor`

Defines the default color of each item's question text.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#00B4B0` |

---

### `answerColor`

Defines the default color of each item's answer text.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#3B3B3B` |

---

### `iconColor`

Defines the default color of each item's chevron (arrow) icon.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#00B4B0` |

---

### `backgroundColor`

Defines the default background color of each item.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#FFFFFF` |

---

### `borderColor`

Defines the default border color around each item.

| Field | Value |
|-------|-------|
| Type | Color |
| Required | ❌ No |
| Default | `#00B4B0` |

---

### `shape`

Defines the default corner shape of each item.

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

The compiler performs the following semantic validations on the `FAQ` block:

- The block must contain at least one `FAQItem` child.
- Each `FAQItem` must provide both `question` and `answer`.
- Unknown or duplicate properties are not allowed.
- Enum properties must contain one of their predefined values.
- Color properties must contain valid color values.

---

## Children

### FAQItem

A `FAQItem` renders a single expandable question-and-answer entry.

#### Hierarchy

| Property | Value |
|----------|-------|
| Parent | `FAQ` |
| Repeatable | ✅ Yes |

#### Properties

| Property | Keyword | Type | Default | Allowed Values |
|----------|---------|------|---------|----------------|
| Question | `question` | String | `""` (required) | Any valid string |
| Answer | `answer` | String | `""` (required) | Any valid string |
| Question Color | `questionColor` | Color | `""` (inherited) | Valid Color |
| Answer Color | `answerColor` | Color | `""` (inherited) | Valid Color |
| Icon Color | `iconColor` | Color | `""` (inherited) | Valid Color |
| Background Color | `backgroundColor` | Color | `""` (inherited) | Valid Color |
| Border Color | `borderColor` | Color | `""` (inherited) | Valid Color |

Item-level properties that are omitted inherit their value from the parent `FAQ` block, and fall back to the parent defaults if the parent does not define them. Item shape always follows the parent `FAQ` block's `shape`.

#### Required Properties

The following properties are mandatory on every `FAQItem`:

- `question`
- `answer`

#### Property Details

##### `question`

The question text displayed in the summary header of the item.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ✅ Yes |

---

##### `answer`

The answer text revealed when the item is expanded.

| Field | Value |
|-------|-------|
| Type | String |
| Required | ✅ Yes |

---

##### `questionColor`, `answerColor`, `iconColor`, `backgroundColor`, `borderColor`

These visual properties behave like their `FAQ` counterparts but apply only to the individual item. When omitted, they inherit the parent block's value.

---

## Rendering Behavior

- Each item is rendered as a card with a `<button>` header containing the question and a chevron icon, and an answer panel below it.
- Clicking a question toggles that item's open/closed state independently — other items remain unaffected.
- The answer panel animates smoothly open and closed via a height transition.
- A chevron icon rotates 180° when an item is open.
- The chevron is tinted by `iconColor`.
- All items start closed by default.
- A small inline script handles the toggling and animation, keeps the chevron and `aria-expanded` state in sync, and re-measures open items on resize so the animation stays correct.

---

## Examples

### Minimal Example

```lkr
FAQ {
    FAQItem { question: "What is Linkora?", answer: "A link-sharing platform." }
}
```

---

### Multiple Items

```lkr
FAQ {
    FAQItem { question: "What is Linkora?", answer: "A link-sharing platform." }
    FAQItem { question: "Is it free?", answer: "Yes, it is free to use." }
    FAQItem { question: "How do I get started?", answer: "Create an account and add your links." }
}
```

---

### Customized Example

```lkr
FAQ {

    questionColor: "#0055AA"

    answerColor: "#333333"

    iconColor: "#0088CC"

    backgroundColor: "#F5F5F5"

    borderColor: "#0055AA"

    shape: slightlyRounded

    FAQItem {
        question: "What is Linkora?"
        answer: "A link-sharing platform."
        backgroundColor: "#FFFFFF"
    }
    FAQItem {
        question: "Is it free?"
        answer: "Yes, it is free to use."
    }

}
```

---

## Invalid Examples

Missing required `question` property:

```lkr
FAQ {
    FAQItem { answer: "A link-sharing platform." }
}
```

❌ Missing required property `question`.

---

Missing required `answer` property:

```lkr
FAQ {
    FAQItem { question: "What is Linkora?" }
}
```

❌ Missing required property `answer`.

---

No children:

```lkr
FAQ {
}
```

❌ The block must contain at least one `FAQItem` child.

---

## Notes

💡 Multiple FAQ items can be open at the same time — toggling one does not close the others.

💡 Clicking a question smoothly animates the answer panel open or closed.

💡 The chevron icon is tinted by `iconColor` and rotates when an item is open.
