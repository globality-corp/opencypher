from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    NodeLabel,
    NodeLabels,
    NonEmptySequence,
    Remove,
    RemoveItem,
    RemoveItems,
    Parameter,
    PropertyExpression,
    PropertyLookup,
    Variable,
)


@parameterized([
    (
        (
            Variable("foo"),
            NodeLabels(
                NodeLabel("Bar"),
                NodeLabel("Baz"),
            ),
        ),
        "REMOVE foo:Bar:Baz",
        dict(),
    ),
    (
        PropertyExpression(
            "foo",
            NonEmptySequence[PropertyLookup](
                PropertyLookup("bar"),
            ),
        ),
        "REMOVE foo . bar",
        dict(),
    ),
    (
        PropertyExpression(
            Parameter("foo", "foo", "value"),
            NonEmptySequence[PropertyLookup](
                PropertyLookup("bar"),
                PropertyLookup("baz"),
            ),
        ),
        "REMOVE $foo . bar . baz",
        dict(foo="value"),
    ),
])
def test_remove(value, query, parameters):
    ast = Remove(
        items=RemoveItems(
            RemoveItem(value),
        ),
    )
    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
    assert_that(
        dict(ast),
        is_(equal_to(parameters)),
    )
