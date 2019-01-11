from hamcrest import (
    assert_that,
    contains,
    empty,
    equal_to,
    has_properties,
    is_,
    none,
)

from opencypher.builder import expr, func, parameters, properties


def test_expr():
    ast = expr("foo")
    assert_that(
        str(ast),
        is_(equal_to("foo")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_expr_alias():
    ast = expr("foo").as_("bar")
    assert_that(
        str(ast),
        is_(equal_to("foo AS bar")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_count():
    ast = func.count(expr("foo"))
    assert_that(
        str(ast),
        is_(equal_to("count(foo)")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_parameters():
    assert_that(
        parameters(foo="bar", this="that"),
        contains(
            has_properties(
                key="foo",
                name="foo",
                value="bar",
            ),
            has_properties(
                key="this",
                name="this",
                value="that",
            ),
        ),
    ),


def test_parameters_empty():
    assert_that(
        parameters(),
        is_(empty()),
    ),


def test_parameters_key_prefix():
    assert_that(
        parameters(key_prefix="key", foo="bar"),
        contains(
            has_properties(
                key="key.foo",
                name="foo",
                value="bar",
            ),
        ),
    ),


def test_parameters_name_prefix():
    assert_that(
        parameters(name_prefix="key", foo="bar"),
        contains(
            has_properties(
                key="foo",
                name="key_foo",
                value="bar",
            ),
        ),
    ),


def test_properties():
    ast = properties(parameters(foo="bar", this="that"))
    assert_that(
        str(ast),
        is_(equal_to("{foo: $foo, this: $this}")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict(
            foo="bar",
            this="that",
        ))),
    )


def test_properties_empty():
    assert_that(
        properties(),
        is_(none()),
    )
