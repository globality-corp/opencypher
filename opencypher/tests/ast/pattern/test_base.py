from hamcrest import assert_that, equal_to, is_

from opencypher.ast import (
    NonEmptyList,
    Pattern,
    PatternElement,
    PatternElementChain,
    PatternPart,
    Variable,
)


def test_pattern():
    ast = Pattern(
        items=NonEmptyList[PatternPart](
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
        is_(equal_to("foo = ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_pattern_chain():
    ast = Pattern(
        items=NonEmptyList[PatternPart](
            PatternPart(
                pattern_element=PatternElement(
                    items=[
                        PatternElementChain(),
                        PatternElementChain(),
                    ],
                ),
            ),
        ),
    )
    assert_that(
        str(ast),
        is_(equal_to("( ) - [ ] - ( ) - [ ] - ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )
