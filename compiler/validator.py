"""Semantic analysis of Linkora documents.

The validator checks every rule defined in the language specification and then
resolves each block's properties to their final values (applying defaults for
omitted optional properties), storing the result in ``Block.resolved``.
"""

from __future__ import annotations

from typing import Optional

from compiler import types
from compiler.ast import Block, Document, KIND_IDENTIFIER, KIND_STRING, Property
from compiler.errors import SemanticError
from compiler.schema import BLOCKS, BlockDef, PropertyDef, ValueType


class Validator:
    """Validates a parsed document against the language schema."""

    def __init__(self, blocks: dict[str, BlockDef] = BLOCKS) -> None:
        self.blocks = blocks

    # -- Public API ---------------------------------------------------------

    def validate(self, document: Document) -> list[SemanticError]:
        errors: list[SemanticError] = []
        sibling_counts: dict[str, int] = {}
        for block in document.blocks:
            self._validate_block(block, parent_name=None, sibling_counts=sibling_counts, errors=errors)
        return errors

    def resolve(self, document: Document) -> Document:
        """Apply defaults so every block has a complete set of properties."""
        for block in document.blocks:
            self._resolve_block(block)
        return document

    # -- Block-level rules ---------------------------------------------------

    def _validate_block(
        self,
        block: Block,
        parent_name: Optional[str],
        sibling_counts: dict[str, int],
        errors: list[SemanticError],
    ) -> None:
        block_def = self.blocks.get(block.name)
        if block_def is None:
            errors.append(
                SemanticError(f"Unknown block '{block.name}'.", block.position)
            )
            return

        if parent_name is None:
            if block_def.parent is not None:
                errors.append(
                    SemanticError(
                        f"Block '{block.name}' is only allowed inside the "
                        f"'{block_def.parent}' block.",
                        block.position,
                    )
                )
        else:
            if block_def.parent != parent_name:
                errors.append(
                    SemanticError(
                        f"Block '{block.name}' is only allowed inside the "
                        f"'{block_def.parent}' block.",
                        block.position,
                    )
                )
            parent_def = self.blocks.get(parent_name)
            if parent_def is not None and block.name not in parent_def.allowed_children:
                errors.append(
                    SemanticError(
                        f"Block '{block.name}' is not allowed inside the "
                        f"'{parent_name}' block.",
                        block.position,
                    )
                )

        if not block_def.repeatable:
            sibling_counts[block.name] = sibling_counts.get(block.name, 0) + 1
            if sibling_counts[block.name] > 1:
                errors.append(
                    SemanticError(
                        f"Block '{block.name}' may appear only once within its parent.",
                        block.position,
                    )
                )

        self._validate_properties(block, block_def, errors)
        self._validate_specific_rules(block, block_def, errors)

        child_counts: dict[str, int] = {}
        for child in block.children:
            self._validate_block(child, block.name, child_counts, errors)

    def _validate_specific_rules(
        self,
        block: Block,
        block_def: BlockDef,
        errors: list[SemanticError],
    ) -> None:
        """Validate block-type-specific rules beyond the generic schema checks."""
        if block.name not in ("SocialMedia", "SocialNetwork"):
            return

        def effective(name: str) -> object:
            prop = block.property(name)
            if prop is not None:
                return prop.value
            return block_def.property(name).default

        columns = effective("columns")
        if columns not in (1, 2, 3, 4):
            errors.append(
                SemanticError(
                    f"Block '{block.name}': 'columns' must be one of 1, 2, 3, 4, "
                    f"found {columns}.",
                    block.position,
                )
            )

        show_title = effective("showTitle")
        show_icon = effective("showIcon")
        if show_title is False and show_icon is False:
            errors.append(
                SemanticError(
                    f"Block '{block.name}': 'showTitle' and 'showIcon' "
                    "cannot both be false.",
                    block.position,
                )
            )

        if columns == 4 and show_title and show_icon:
            errors.append(
                SemanticError(
                    f"Block '{block.name}': 'columns' can only be 4 when either "
                    "'showTitle' or 'showIcon' is false.",
                    block.position,
                )
            )

        if not block.children:
            errors.append(
                SemanticError(
                    f"Block '{block.name}' must contain at least one "
                    f"'{block_def.allowed_children[0]}' child.",
                    block.position,
                )
            )

    # -- Property-level rules -------------------------------------------------

    def _validate_properties(
        self,
        block: Block,
        block_def: BlockDef,
        errors: list[SemanticError],
    ) -> None:
        present: set[str] = set()

        for prop in block.properties:
            prop_def = block_def.property(prop.name)
            if prop_def is None:
                errors.append(
                    SemanticError(
                        f"Unknown property '{prop.name}' inside block '{block.name}'.",
                        prop.position,
                    )
                )
                continue
            if prop.name in present:
                errors.append(
                    SemanticError(
                        f"Duplicate property '{prop.name}' inside block '{block.name}'.",
                        prop.position,
                    )
                )
                continue
            present.add(prop.name)
            self._validate_value(prop, prop_def, block, errors)

        for prop_def in block_def.properties.values():
            if prop_def.required and prop_def.name not in present:
                errors.append(
                    SemanticError(
                        f"Block '{block.name}' is missing the required property "
                        f"'{prop_def.name}'.",
                        block.position,
                    )
                )

    def _validate_value(
        self,
        prop: Property,
        prop_def: PropertyDef,
        block: Block,
        errors: list[SemanticError],
    ) -> None:
        value = prop.value

        def fail(message: str) -> None:
            errors.append(
                SemanticError(
                    f"Property '{prop.name}' inside block '{block.name}': {message}",
                    prop.position,
                )
            )

        expected = prop_def.type
        if expected is ValueType.STRING:
            if not isinstance(value, str):
                fail(f"expected a String value, found {_describe(prop)}.")
        elif expected is ValueType.NUMBER:
            if not types.is_number(value):
                fail(f"expected a Number value, found {_describe(prop)}.")
        elif expected is ValueType.BOOLEAN:
            if not types.is_boolean(value):
                fail(f"expected a Boolean value, found {_describe(prop)}.")
        elif expected is ValueType.COLOR:
            if not types.is_color(value):
                fail(f"expected a valid Color value, found {_describe(prop)}.")
        elif expected is ValueType.URL:
            if not types.is_url(value):
                fail(
                    "expected a valid HTTP or HTTPS URL "
                    f"(for example \"https://example.com\"), found {_describe(prop)}."
                )
        elif expected is ValueType.FILE:
            if not types.is_file_path(value):
                fail(f"expected a relative file path, found {_describe(prop)}.")
        elif expected is ValueType.IMAGE:
            if not types.is_image(value):
                fail(
                    "expected an image URL or a relative file path with an image "
                    f"extension (.jpg, .png, .svg, .gif, .webp), found {_describe(prop)}."
                )
        elif expected is ValueType.ENUM:
            if prop.kind == KIND_IDENTIFIER and value in prop_def.enum_values:
                return
            if prop.kind == KIND_STRING:
                fail("enum values must not be enclosed in quotation marks.")
            else:
                allowed = ", ".join(prop_def.enum_values)
                fail(
                    f"'{value}' is not a valid value. "
                    f"Allowed values: {allowed}."
                )

    # -- Default resolution -----------------------------------------------------

    def _resolve_block(self, block: Block) -> None:
        block_def = self.blocks.get(block.name)
        if block_def is None:
            return

        resolved: dict[str, object] = {}
        for prop in block.properties:
            prop_def = block_def.property(prop.name)
            if prop_def is not None:
                resolved[prop.name] = prop.value

        for prop_def in block_def.properties.values():
            resolved.setdefault(prop_def.name, prop_def.default)

        block.resolved = resolved

        for child in block.children:
            self._resolve_block(child)


def _describe(prop: Property) -> str:
    if prop.kind == "STRING":
        return prop.text
    return f"'{prop.text}'"
