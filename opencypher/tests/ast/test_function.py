from hamcrest import assert_that, equal_to, is_

from opencypher.ast import (
    Expression,
    FunctionInvocation,
    NonEmptySequence,
)


def test_function_invocation():
    ast = FunctionInvocation(
        Expression("foo"),
        expressions=NonEmptySequence[Expression](
            Expression("bar"),
        ),
    )
    assert_that(
        str(ast),
        is_(equal_to("foo(bar)")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_distinct_function_invocation():
    ast = FunctionInvocation(
        Expression("foo"),
        expressions=NonEmptySequence[Expression](
            Expression("bar"),
        ),
        distinct=True,
    )
    assert_that(
        str(ast),
        is_(equal_to("foo(DISTINCT bar)")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )
