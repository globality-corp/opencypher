from hamcrest import assert_that, equal_to, is_

from opencypher.builder import (
    create,
    delete,
    expr,
    match,
    merge,
    node,
    parameters,
    ret,
    set,
)


def test_create():
    ast = create(node())
    assert_that(
        str(ast),
        is_(equal_to("CREATE ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_create():
    ast = create(node()).create(node())
    assert_that(
        str(ast),
        is_(equal_to("CREATE ( ) CREATE ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_delete():
    ast = create(node()).delete("foo")
    assert_that(
        str(ast),
        is_(equal_to("CREATE ( ) DELETE foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_match():
    ast = create(node()).match(node())
    assert_that(
        str(ast),
        is_(equal_to("MATCH ( ) CREATE ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_merge():
    ast = create(node()).merge(node())
    assert_that(
        str(ast),
        is_(equal_to("CREATE ( ) MERGE ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_ret():
    ast = create(node()).ret("foo")
    assert_that(
        str(ast),
        is_(equal_to("CREATE ( ) RETURN foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_set():
    ast = create(node()).set(*parameters(foo="bar"))
    assert_that(
        str(ast),
        is_(equal_to("CREATE ( ) SET foo = $foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict(foo="bar"))),
    )


def test_delete():
    ast = delete("foo")
    assert_that(
        str(ast),
        is_(equal_to("DELETE foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match():
    ast = match(node()).ret("foo")
    assert_that(
        str(ast),
        is_(equal_to("MATCH ( ) RETURN foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match_create():
    ast = match(node()).create(node())
    assert_that(
        str(ast),
        is_(equal_to("MATCH ( ) CREATE ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match_delete():
    ast = match(node()).delete("foo")
    assert_that(
        str(ast),
        is_(equal_to("MATCH ( ) DELETE foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match_match():
    ast = match(node()).match(node()).ret("foo")
    assert_that(
        str(ast),
        is_(equal_to("MATCH ( ) MATCH ( ) RETURN foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match_merge():
    ast = match(node()).merge(node())
    assert_that(
        str(ast),
        is_(equal_to("MATCH ( ) MERGE ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match_set():
    ast = match(node()).set(*parameters(foo="bar"))
    assert_that(
        str(ast),
        is_(equal_to("MATCH ( ) SET foo = $foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict(foo="bar"))),
    )


def test_merge():
    ast = merge(node())
    assert_that(
        str(ast),
        is_(equal_to("MERGE ( )")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_ret():
    ast = ret(expr(1))
    assert_that(
        str(ast),
        is_(equal_to("RETURN 1")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_set():
    ast = set(*parameters(foo="bar"))
    assert_that(
        str(ast),
        is_(equal_to("SET foo = $foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict(foo="bar"))),
    )
