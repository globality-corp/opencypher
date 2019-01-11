from typing import Tuple

from opencypher.ast import (
    Create,
    Delete,
    Expression,
    Match,
    Merge,
    NodeLabel,
    NodeLabels,
    NonEmptySequence,
    Parameter,
    Pattern,
    PatternElement,
    PatternPart,
    PropertyExpression,
    PropertyLookup,
    Remove,
    RemoveItem,
    RemoveItems,
    Set,
    SetItem,
    SetItems,
    SetVariableItem,
    Variable,
    Unwind,
)
from opencypher.builder import expr


class ClauseFactory:

    @classmethod
    def create(cls, pattern_element: PatternElement) -> Create:
        return Create(
            pattern=Pattern(
                items=NonEmptySequence[PatternPart](
                    PatternPart(pattern_element),
                ),
            ),
        )

    @classmethod
    def delete(cls,
               expression: str,
               *expressions: str,
               detach: bool = False) -> Delete:
        return Delete(
            items=NonEmptySequence[Expression](
                expr(expression),
                *(
                    expr(item)
                    for item in expressions
                ),
            ),
            detach=detach,
        )

    @classmethod
    def match(cls, pattern_element: PatternElement) -> Match:
        return Match(
            pattern=Pattern(
                items=NonEmptySequence[PatternPart](
                    PatternPart(pattern_element),
                ),
            ),
        )

    @classmethod
    def merge(cls, pattern_element: PatternElement) -> Merge:
        return Merge(
            pattern_part=PatternPart(pattern_element),
        )

    @classmethod
    def remove_item(cls, head: str, tail: str) -> RemoveItem:
        if ":" in tail:
            node_labels = [
                NodeLabel(item.lstrip(":"))
                for item in tail.split()
            ]
            return RemoveItem(
                value=(
                    Variable(head),
                    NodeLabels(
                        node_labels[0],
                        *node_labels[1:],
                    ),
                ),
            )
        else:
            property_lookups = [
                PropertyLookup(item)
                for item in tail.split(".")
            ]
            return RemoveItem(
                value=PropertyExpression(
                    value=head,
                    properties=NonEmptySequence[PropertyLookup](
                        property_lookups[0],
                        *property_lookups[1:],
                    ),
                ),
            )

    @classmethod
    def remove(cls, target: Tuple[str, str], *targets: Tuple[str, str]) -> Remove:
        return Remove(
            items=RemoveItems(
                cls.remove_item(*target),
                *(
                    cls.remove_item(*item)
                    for item in targets
                ),
            ),
        )

    @classmethod
    def set_item(cls, parameter: Parameter) -> SetItem:
        return SetVariableItem(
            target=Variable(parameter.key),
            value=expr(parameter),
        )

    @classmethod
    def set(cls, parameter: Parameter, *parameters: Parameter) -> Set:
        return Set(
            items=SetItems(
                cls.set_item(parameter),
                *(
                    cls.set_item(item)
                    for item in parameters
                ),
            ),
        )

    @classmethod
    def unwind(cls, expression: Expression, variable: Variable) -> Unwind:
        return Unwind(
            expression=expression,
            variable=variable,
        )
