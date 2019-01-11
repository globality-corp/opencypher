from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    Expression,
    Parameter,
    Unwind,
    Variable,
)


@parameterized([
    (
        "foo", "bar",
        "UNWIND foo AS bar",
        dict(),
    ),
    (
        Parameter("foo", "foo", "foo"), "bar",
        "UNWIND $foo AS bar",
        dict(foo="foo"),
    ),
])
def test_match(expression, variable, query, parameters):
    ast = Unwind(
        expression=Expression(expression),
        variable=Variable(variable),
    )
    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
    assert_that(
        dict(ast),
        is_(equal_to(parameters)),
    )
