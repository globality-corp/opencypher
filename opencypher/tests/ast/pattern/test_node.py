from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    MapLiteral,
    NodeLabel,
    NodePattern,
    NonEmptySequence,
    Parameter,
    Variable,
)


@parameterized([
    (
        "foo", ["Bar"], dict(this="that"),
        "( foo :Bar { this: $this } )",
        dict(this="that"),
    ),
    (
        None, ["Bar", "Baz"], dict(this="that"),
        "( :Bar :Baz { this: $this } )",
        dict(this="that"),
    ),
    (
        "foo", None, dict(this="that"),
        "( foo { this: $this } )",
        dict(this="that"),
    ),
    (
        "foo", ["Bar"], None,
        "( foo :Bar )",
        dict(),
    ),
    (
        "foo", None, None,
        "( foo )",
        dict(),
    ),
    (
        None, ["Bar"], None,
        "( :Bar )",
        dict(),
    ),
    (
        None, None, dict(this="that"),
        "( { this: $this } )",
        dict(this="that"),
    ),
    (
        None, None, None,
        "( )",
        dict(),
    ),
])
def test_relationship_detail(variable, labels, properties, query, parameters):
    ast = NodePattern(
        variable=Variable(variable) if variable is not None else None,
        labels=NonEmptySequence[NodeLabel](
            NodeLabel(labels[0]),
            *(
                NodeLabel(label)
                for label in labels[1:]
            ),
        ) if labels else None,
        properties=MapLiteral([
            (key, Parameter(key, key, value))
            for key, value in properties.items()
        ]) if properties else None,
    )
    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
    assert_that(
        dict(ast),
        is_(equal_to(parameters)),
    )
