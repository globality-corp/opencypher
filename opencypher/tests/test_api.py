from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

from opencypher.api import (
    asc,
    match,
    node,
    parameters,
    properties,
)


def test_api():
    ast = match(
        node(
            "foo",
            "Foo",
            properties=properties(
                parameters(
                    name_prefix="foo",
                    bar="baz",
                ),
            ),
        ).rel_in(
            None,
            "Bar",
        ).node(
            "baz",
            "Baz",
            properties=properties(
                parameters(
                    name_prefix="baz",
                    bar="foo",
                ),
            ),
        ),
    ).delete(
        "foo",
        "baz",
    ).ret(
        "foo",
        "baz",
        order=asc("foo", "bar"),
    )

    assert_that(
        str(ast),
        is_(equal_to(
            "MATCH ( foo :Foo { bar: $foo_bar } ) - [ :Bar ] -> ( baz :Baz { bar: $baz_bar } ) "
            "DELETE foo, baz "
            "RETURN foo, baz ORDER BY foo ASCENDING, bar ASCENDING",
        )),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict(
            foo_bar="baz",
            baz_bar="foo",
        ))),
    )
