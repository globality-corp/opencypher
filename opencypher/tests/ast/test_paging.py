from hamcrest import assert_that, equal_to, is_

from opencypher.ast import Expression, Limit, Skip


def test_limit():
    ast = Limit(Expression(1))
    assert_that(
        str(ast),
        is_(equal_to("LIMIT 1")),
    )


def test_skip():
    ast = Skip(Expression(1))
    assert_that(
        str(ast),
        is_(equal_to("SKIP 1")),
    )
