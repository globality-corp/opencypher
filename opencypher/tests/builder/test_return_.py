from hamcrest import assert_that, equal_to, is_

from opencypher.builder import asc, desc, order


def test_asc():
    ast = asc("foo")
    assert_that(
        str(ast),
        is_(equal_to("ORDER BY foo ASCENDING")),
    )


def test_desc():
    ast = desc("foo")
    assert_that(
        str(ast),
        is_(equal_to("ORDER BY foo DESCENDING")),
    )


def test_order():
    ast = order("foo")
    assert_that(
        str(ast),
        is_(equal_to("ORDER BY foo")),
    )
