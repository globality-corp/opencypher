from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.builder import (
    create,
    delete,
    expr,
    match,
    merge,
    node,
    parameters,
    remove,
    ret,
    set,
    unwind,
    var,
)


def test_create():
    ast = create(node())
    assert_that(
        str(ast),
        is_(equal_to("CREATE ()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_create():
    ast = create(node()).create(node())
    assert_that(
        str(ast),
        is_(equal_to("CREATE () CREATE ()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_delete():
    ast = create(node()).delete("foo")
    assert_that(
        str(ast),
        is_(equal_to("CREATE () DELETE foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_match():
    ast = create(node()).match(node())
    assert_that(
        str(ast),
        is_(equal_to("MATCH () CREATE ()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_merge():
    ast = create(node()).merge(node())
    assert_that(
        str(ast),
        is_(equal_to("CREATE () MERGE ()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_ret():
    ast = create(node()).ret("foo")
    assert_that(
        str(ast),
        is_(equal_to("CREATE () RETURN foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_create_set():
    ast = create(node()).set(*parameters(foo="bar"))
    assert_that(
        str(ast),
        is_(equal_to("CREATE () SET foo = $foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict(foo="bar"))),
    )


def test_create_union():
    ast = create(node()).union_all(create(node()))
    assert_that(
        str(ast),
        is_(equal_to("CREATE () UNION ALL CREATE ()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
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
        is_(equal_to("MATCH () RETURN foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match_create():
    ast = match(node()).create(node())
    assert_that(
        str(ast),
        is_(equal_to("MATCH () CREATE ()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match_delete():
    ast = match(node()).delete("foo")
    assert_that(
        str(ast),
        is_(equal_to("MATCH () DELETE foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match_match():
    ast = match(node()).match(node()).ret("foo")
    assert_that(
        str(ast),
        is_(equal_to("MATCH () MATCH () RETURN foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match_merge():
    ast = match(node()).merge(node())
    assert_that(
        str(ast),
        is_(equal_to("MATCH () MERGE ()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_match_set():
    ast = match(node()).set(*parameters(foo="bar"))
    assert_that(
        str(ast),
        is_(equal_to("MATCH () SET foo = $foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict(foo="bar"))),
    )


def test_match_union():
    ast = match(
        node("foo", "Foo", {"bar": "baz"}),
    ).ret("foo").union(
        match(
            node("bar", "Bar", {"foo": "baz"}),
        ).ret(
            "bar",
        )
    )
    assert_that(
        str(ast),
        is_(equal_to(
            "MATCH (foo:Foo {bar: $foo_bar}) "
            "RETURN foo "
            "UNION "
            "MATCH (bar:Bar {foo: $bar_foo}) "
            "RETURN bar",
        )),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict(
            foo_bar="baz",
            bar_foo="baz",
        ))),
    )


def test_merge():
    ast = merge(node())
    assert_that(
        str(ast),
        is_(equal_to("MERGE ()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


@parameterized([
    (
        ("foo", "bar"),
        "REMOVE foo.bar",
        dict(),
    ),
    (
        ("foo", "bar.baz"),
        "REMOVE foo.bar.baz",
        dict(),
    ),
    (
        ("foo", ":Bar"),
        "REMOVE foo:Bar",
        dict(),
    ),
    (
        ("foo", ":Bar :Baz"),
        "REMOVE foo:Bar:Baz",
        dict(),
    ),
])
def test_remove(target, query, parameters):
    ast = remove(target)
    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
    assert_that(
        dict(ast),
        is_(equal_to(parameters)),
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


def test_unwind():
    ast = unwind(expr("foo"), var("bar")).ret("bar")
    assert_that(
        str(ast),
        is_(equal_to("UNWIND foo AS bar RETURN bar")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_unwind_create():
    ast = unwind(expr("foo"), var("bar")).create(node())
    assert_that(
        str(ast),
        is_(equal_to("UNWIND foo AS bar CREATE ()")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )
