from hamcrest import assert_that, equal_to, is_

from opencypher.ast import (
    NonEmptySequence,
    Pattern,
    PatternElement,
    PatternElementChain,
    PatternPart,
    RelationshipPattern,
    RelationshipDetail,
    Variable,
)


def test_pattern():
    ast = Pattern(
        items=NonEmptySequence[PatternPart](
            PatternPart(
                pattern_element=PatternElement(
                    items=[],
                ),
                variable=Variable("foo"),
            ),
        ),
    )
    assert_that(
        str(ast),
        is_(equal_to("foo = ()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_pattern_chain():
    ast = Pattern(
        items=NonEmptySequence[PatternPart](
            PatternPart(
                pattern_element=PatternElement(
                    items=[
                        PatternElementChain(),
                        PatternElementChain(),
                        PatternElementChain(
                            relationship_pattern=RelationshipPattern(
                                detail=RelationshipDetail(),
                            )
                        ),
                    ],
                ),
            ),
        ),
    )
    assert_that(
        str(ast),
        is_(equal_to("()--()--()-[]-()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )
