from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    Expression,
    Match,
    NonEmptySequence,
    Pattern,
    PatternPart,
    Where,
)


@parameterized([
    (
        False, None,
        "MATCH ()",
        dict(),
    ),
    (
        True, None,
        "OPTIONAL MATCH ()",
        dict(),
    ),
    (
        False, "foo",
        "MATCH () WHERE foo",
        dict(),
    ),
    (
        True, "foo",
        "OPTIONAL MATCH () WHERE foo",
        dict(),
    ),
])
def test_match(optional, where, query, parameters):
    ast = Match(
        pattern=Pattern(
            items=NonEmptySequence[PatternPart](
                PatternPart(),
            )
        ),
        optional=optional,
        where=Where(Expression(where)) if where is not None else None,
    )
    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
    assert_that(
        dict(ast),
        is_(equal_to(parameters)),
    )
