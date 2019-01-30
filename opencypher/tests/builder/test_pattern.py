from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.builder import node


def test_node():
    ast = node()

    assert_that(
        str(ast),
        is_(equal_to("()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


@parameterized([
    (
        None,
        "()-[]-()",
        dict(),
    ),
    (
        (),
        "()-[*]-()",
        dict(),
    ),
    (
        (1, ),
        "()-[*1]-()",
        dict(),
    ),
    (
        (1, 2),
        "()-[*1..2]-()",
        dict(),
    ),
])
def test_rel(length, query, parameters):
    ast = node().rel(length=length).node()

    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
    assert_that(
        dict(ast),
        is_(equal_to(parameters)),
    )


def test_rel_in():
    ast = node().rel_in().node()

    assert_that(
        str(ast),
        is_(equal_to("()<-[]-()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_rel_out():
    ast = node().rel_out().node()

    assert_that(
        str(ast),
        is_(equal_to("()-[]->()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )
