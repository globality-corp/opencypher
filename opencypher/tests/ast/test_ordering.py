from hamcrest import assert_that, equal_to, is_

from opencypher.ast import Expression, NonEmptyList, Order, SortItem, SortOrder


def test_order():
    ast = Order(
        items=NonEmptyList[SortItem](
            SortItem(
                expression=Expression("foo"),
                order=SortOrder.DESCENDING,
            ),
        ),
    )
    assert_that(
        str(ast),
        is_(equal_to("ORDER BY foo DESCENDING")),
    )
