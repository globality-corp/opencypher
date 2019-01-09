from hamcrest import assert_that, equal_to, is_

from opencypher.ast import (
    Expression,
    ExpressionAlias,
    FunctionInvocation,
    NonEmptyList,
    Parameter,
    Variable,
)


def test_function_invocation():
    ast = FunctionInvocation(
        Expression("foo"),
        expressions=NonEmptyList[Expression](
            "bar",
        ),
    )
    assert_that(
        str(ast),
        is_(equal_to("foo( bar )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_distinct_function_invocation():
    ast = FunctionInvocation(
        Expression("foo"),
        expressions=NonEmptyList[Expression](
            "bar",
        ),
        distinct=True,
    )
    assert_that(
        str(ast),
        is_(equal_to("foo( DISTINCT bar )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_expression():
    ast = Expression("foo")
    assert_that(
        str(ast),
        is_(equal_to("foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_expression_parameter():
    ast = Expression(
        Parameter("key", "name", "value"),
    )
    assert_that(
        str(ast),
        is_(equal_to("$name")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict(name="value"))),
    )


def test_expression_function_invocation():
    ast = Expression(
        FunctionInvocation(
            Expression("foo"),
            expressions=NonEmptyList[Expression](
                Expression(
                    "bar",
                ),
            ),
        )
    )
    assert_that(
        str(ast),
        is_(equal_to("foo( bar )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_expression_alias():
    ast = ExpressionAlias(
        Expression("foo"),
        Variable("bar"),
    )
    assert_that(
        str(ast),
        is_(equal_to("foo AS bar")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )
