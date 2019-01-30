from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    Expression,
    ExpressionAlias,
    Limit,
    NonEmptySequence,
    Order,
    ReturnBody,
    ReturnItem,
    Skip,
    SortItem,
    With,
    Where,
)


@parameterized([
    (
        False, ["foo", "bar", "baz"], None, None, None, None,
        "WITH foo, bar AS baz",
    ),
    (
        False, ["()", "foo"], None, None, None, None,
        "WITH () AS foo",
    ),
    (
        True, ["()"], None, None, None, None,
        "WITH DISTINCT ()",
    ),
    (
        True, ["()", "foo"], None, None, None, None,
        "WITH DISTINCT () AS foo",
    ),
    (
        True, ["()"], None, None, None, "Bar",
        "WITH DISTINCT () WHERE Bar",
    ),
    (
        True, ["()", "Foo"], None, None, None, "Bar",
        "WITH DISTINCT () AS Foo WHERE Bar",
    ),
    (
        False, ["otherPerson", "foaf"], None, None, None, "foaf > 1",
        "WITH otherPerson AS foaf WHERE foaf > 1",
    ),
    (
        False, ["otherPerson", "count(*)", "foaf"], None, None, None, "foaf > 1",
        "WITH otherPerson, count(*) AS foaf WHERE foaf > 1",
    ),
    (
        False, ["n"], "n.name DESC", None, 3, None,
        "WITH n ORDER BY n.name DESC LIMIT 3",
    ),
])
def test_with(distinct, items, order, skip, limit, where, query):

    ast = With(
        body=ReturnBody(
            items=NonEmptySequence[ReturnItem](
                *(
                    Expression(value)
                    for value in items[:-2]
                ),
                (
                    ExpressionAlias(items[-2], items[-1])
                )
            ) if len(items) > 1
            else NonEmptySequence[ReturnItem](Expression(items[0])),
            order=Order(items=NonEmptySequence[SortItem](SortItem(Expression(order)))) if order else None,
            skip=Skip(Expression(skip)) if skip is not None else None,
            limit=Limit(Expression(limit)) if limit is not None else None,
        ),
        distinct=distinct,
        where=Where(Expression(where)) if where is not None else None,
    )
    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
