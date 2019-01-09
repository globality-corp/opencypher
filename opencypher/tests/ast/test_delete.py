from hamcrest import assert_that, equal_to, is_

from opencypher.ast import (
    Delete,
    Expression,
    NonEmptyList,
)


def test_delete():
    ast = Delete(
        items=NonEmptyList[Expression](
            Expression("foo"),
        ),
    )
    assert_that(
        str(ast),
        is_(equal_to("DELETE foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_detach_delete():
    ast = Delete(
        items=NonEmptyList[Expression](
            Expression("foo"),
        ),
        detach=True,
    )
    assert_that(
        str(ast),
        is_(equal_to("DETACH DELETE foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )
