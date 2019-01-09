from opencypher.ast import (
    Create,
    Delete,
    Expression,
    Match,
    Merge,
    NonEmptySequence,
    Parameter,
    Pattern,
    PatternElement,
    PatternPart,
    Set,
    SetItem,
    Variable,
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
    def set(cls, parameter: Parameter, *parameters: Parameter) -> Set:
        def set_item(parameter: Parameter) -> SetItem:
            return SetItem(
                variable=Variable(parameter.key),
                expression=expr(parameter),
            )

        return Set(
            items=NonEmptySequence[SetItem](
                set_item(parameter),
                *(
                    set_item(item)
                    for item in parameters
                ),
            ),
        )
