from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    Expression,
    Limit,
    NonEmptyList,
    Order,
    Return,
    ReturnBody,
    ReturnItem,
    Skip,
    SortItem,
)


@parameterized([
    (
        False, ["*"], None, None, None,
        "RETURN *",
    ),
    (
        False, ["foo", "bar"], None, None, None,
        "RETURN foo, bar",
    ),
    (
        False, ["foo"], None, None, 1,
        "RETURN foo LIMIT 1",
    ),
    (
        False, ["foo"], None, 2, None,
        "RETURN foo SKIP 2",
    ),
    (
        False, ["foo"], "foo", None, None,
        "RETURN foo ORDER BY foo",
    ),
    (
        False, ["foo"], None, 2, 1,
        "RETURN foo SKIP 2 LIMIT 1",
    ),
    (
        False, ["foo"], "foo", 2, None,
        "RETURN foo ORDER BY foo SKIP 2",
    ),
    (
        False, ["foo"], "foo", None, 1,
        "RETURN foo ORDER BY foo LIMIT 1",
    ),
    (
        False, ["foo"], "foo", 2, 1,
        "RETURN foo ORDER BY foo SKIP 2 LIMIT 1",
    ),
    (
        True, ["foo"], None, None, None,
        "RETURN DISTINCT foo",
    ),
])
def test_return(distinct, items, order, skip, limit, query):
    ast = Return(
        ReturnBody(
            items=NonEmptyList[ReturnItem](
                Expression(items[0]),
                *(
                    Expression(value)
                    for value in items[1:]
                ),
            ),
            order=Order(items=NonEmptyList[SortItem](SortItem(Expression(order)))) if order else None,
            skip=Skip(Expression(skip)) if skip is not None else None,
            limit=Limit(Expression(limit)) if limit is not None else None,
        ),
        distinct=distinct,
    )
    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
