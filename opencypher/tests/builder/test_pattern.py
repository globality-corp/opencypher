from hamcrest import assert_that, equal_to, is_

from opencypher.builder import node


def test_node():
    ast = node()

    assert_that(
        str(ast),
        is_(equal_to("( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_rel():
    ast = node().rel().node()

    assert_that(
        str(ast),
        is_(equal_to("( ) - [ ] - ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_rel_in():
    ast = node().rel_in().node()

    assert_that(
        str(ast),
        is_(equal_to("( ) - [ ] -> ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_rel_out():
    ast = node().rel_out().node()

    assert_that(
        str(ast),
        is_(equal_to("( ) <- [ ] - ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )
