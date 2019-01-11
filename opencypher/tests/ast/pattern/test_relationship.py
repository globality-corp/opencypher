from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    MapLiteral,
    RangeLiteral,
    RelationshipDetail,
    RelationshipPattern,
    RelationshipPatternType,
    RelTypeName,
    NonEmptySequence,
    Parameter,
    Variable,
)


@parameterized([
    (
        1, 2, "*1..2",
    ),
    (
        1, None, "*1",
    ),
    (
        None, None, "*",
    ),
])
def test_range_literal(start, end, query):
    ast = RangeLiteral(start, end)
    assert_that(
        str(ast),
        is_(equal_to(query)),
    )


@parameterized([
    (
        "foo", ["Bar"], (1, 2), dict(this="that"),
        "[foo :Bar *1..2 {this: $this}]",
        dict(this="that"),
    ),
    (
        "foo", ["Bar"], None, dict(this="that"),
        "[foo :Bar {this: $this}]",
        dict(this="that"),
    ),
    (
        None, ["Bar", "Baz"], None, dict(this="that"),
        "[:Bar|:Baz {this: $this}]",
        dict(this="that"),
    ),
    (
        "foo", None, None, dict(this="that"),
        "[foo {this: $this}]",
        dict(this="that"),
    ),
    (
        "foo", ["Bar"], None, None,
        "[foo :Bar]",
        dict(),
    ),
    (
        "foo", None, None, None,
        "[foo]",
        dict(),
    ),
    (
        None, ["Bar"], None, None,
        "[:Bar]",
        dict(),
    ),
    (
        None, None, (1, 2), None,
        "[*1..2]",
        dict(),
    ),
    (
        None, None, None, dict(this="that"),
        "[{this: $this}]",
        dict(this="that"),
    ),
    (
        None, None, None, None,
        "[]",
        dict(),
    ),
])
def test_relationship_detail(variable, types, length, properties, query, parameters):
    ast = RelationshipDetail(
        variable=Variable(variable) if variable is not None else None,
        types=NonEmptySequence[RelTypeName](
            RelTypeName(types[0]),
            *(
                RelTypeName(type_)
                for type_ in types[1:]
            ),
        ) if types else None,
        length=RangeLiteral(
            start=length[0],
            end=length[1],
        ) if length else None,
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


@parameterized([
    (
        RelationshipPatternType.BOTH,
        RelationshipDetail(),
        "<-[]->",
        dict(),
    ),
    (
        RelationshipPatternType.BOTH,
        None,
        "<-->",
        dict(),
    ),
    (
        RelationshipPatternType.IN,
        RelationshipDetail(),
        "-[]->",
        dict(),
    ),
    (
        RelationshipPatternType.IN,
        None,
        "-->",
        dict(),
    ),
    (
        RelationshipPatternType.NONE,
        RelationshipDetail(),
        "-[]-",
        dict(),
    ),
    (
        RelationshipPatternType.NONE,
        None,
        "--",
        dict(),
    ),
    (
        RelationshipPatternType.OUT,
        RelationshipDetail(),
        "<-[]-",
        dict(),
    ),
    (
        RelationshipPatternType.OUT,
        None,
        "<--",
        dict(),
    ),
])
def test_relationship_pattern(pattern_type, detail, query, parameters):
    ast = RelationshipPattern(
        pattern_type=pattern_type,
        detail=detail,
    )
    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
    assert_that(
        dict(ast),
        is_(equal_to(parameters)),
    )
