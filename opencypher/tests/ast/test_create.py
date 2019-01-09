from hamcrest import assert_that, equal_to, is_

from opencypher.ast import (
    Create,
    NonEmptyList,
    Pattern,
    PatternPart,
)


def test_create():
    ast = Create(
        pattern=Pattern(
            items=NonEmptyList[PatternPart](
                PatternPart(),
            ),
        ),
    )
    assert_that(
        str(ast),
        is_(equal_to("CREATE ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )
