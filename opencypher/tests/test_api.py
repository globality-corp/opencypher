from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

from opencypher.api import (
    asc,
    delete,
    match,
    node,
    parameters,
    properties,
    ret,
)


class TestAPI:

    def setup(self):
        self.node = node(
            "foo",
            "Foo",
            properties=properties(
                parameters(
                    name_prefix="foo",
                    bar="baz",
                ),
            ),
        )

    def test_node(self):
        assert_that(
            str(self.node),
            is_(equal_to("( foo :Foo { bar: $foo_bar } )")),
        )

    def test_rel(self):
        assert_that(
            str(self.node.rel("bar", "Bar").node("baz", "Baz")),
            is_(equal_to("( foo :Foo { bar: $foo_bar } ) - [ bar :Bar ] - ( baz :Baz )")),
        )

    def test_rel_in(self):
        assert_that(
            str(self.node.rel_in("bar", "Bar").node("baz", "Baz")),
            is_(equal_to("( foo :Foo { bar: $foo_bar } ) - [ bar :Bar ] -> ( baz :Baz )")),
        )

    def test_rel_out(self):
        assert_that(
            str(self.node.rel_out("bar", "Bar").node("baz", "Baz")),
            is_(equal_to("( foo :Foo { bar: $foo_bar } ) <- [ bar :Bar ] - ( baz :Baz )")),
        )

    def test_delete(self):
        query = delete("foo")
        assert_that(
            str(query),
            is_(equal_to("DELETE foo")),
        )

    def test_ret(self):
        query = ret("foo")
        assert_that(
            str(query),
            is_(equal_to("RETURN foo")),
        )

    def test_ret_skip_limit(self):
        query = ret("foo", skip=10, limit=20)
        assert_that(
            str(query),
            is_(equal_to("RETURN foo SKIP 10 LIMIT 20")),
        )

    def test_ret_order(self):
        query = ret("foo", order=asc("bar"))
        assert_that(
            str(query),
            is_(equal_to("RETURN foo ORDER BY bar ASCENDING")),
        )

    def test_match(self):
        query = match(self.node).ret("foo")
        assert_that(
            str(query),
            is_(equal_to("MATCH ( foo :Foo { bar: $foo_bar } ) RETURN foo")),
        )
        assert_that(
            dict(query),
            is_(equal_to(dict(
                foo_bar="baz")
            )),
        )
