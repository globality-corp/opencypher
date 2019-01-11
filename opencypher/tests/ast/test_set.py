from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    Expression,
    NodeLabel,
    NodeLabels,
    NonEmptySequence,
    PropertyExpression,
    PropertyLookup,
    Set,
    SetItems,
    SetPropertyItem,
    SetVariableItem,
    SetVariableNodeLabelsItem,
    Variable,
)


def test_set_property_item():
    ast = SetPropertyItem(
        target=PropertyExpression(
            value="foo",
            properties=NonEmptySequence[PropertyLookup](
                PropertyLookup("bar"),
            ),
        ),
        value=Expression("baz"),
    )

    assert_that(
        str(ast),
        is_(equal_to("foo.bar = baz")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


@parameterized([
    (
        "foo", "bar", False,
        "foo = bar",
        dict()
    ),
    (
        "foo", "bar", True,
        "foo += bar",
        dict()
    ),
])
def test_set_variable_item(variable, expression, mutate, query, parameters):
    ast = SetVariableItem(
        target=Variable(variable),
        value=Expression(expression),
        mutate=mutate,
    )

    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
    assert_that(
        dict(ast),
        is_(equal_to(parameters)),
    )


def test_set_variable_node_labels_item():
    ast = SetVariableNodeLabelsItem(
        target=Variable("foo"),
        value=NodeLabels(
            NodeLabel("Bar"),
        ),
    )

    assert_that(
        str(ast),
        is_(equal_to("foo:Bar")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )


def test_set():
    ast = Set(
        items=SetItems(
            SetVariableNodeLabelsItem(
                target=Variable("foo"),
                value=NodeLabels(
                    NodeLabel("Bar"),
                ),
            ),
            *(
                SetPropertyItem(
                    target=PropertyExpression(
                        value="foo",
                        properties=NonEmptySequence[PropertyLookup](
                            PropertyLookup("bar"),
                        ),
                    ),
                    value=Expression("baz"),
                ),
            ),
        ),
    )
    assert_that(
        str(ast),
        is_(equal_to("SET foo:Bar, foo.bar = baz")),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict())),
    )
