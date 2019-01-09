from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    Cypher,
    Expression,
    Match,
    Merge,
    NodePattern,
    NonEmptyList,
    PatternPart,
    SinglePartReadQuery,
    SinglePartWriteQuery,
    Return,
    ReturnBody,
    ReturnItem,
)


@parameterized([
    (
        None,
        "RETURN foo",
        dict(),
    ),
    (
        Match(pattern=NodePattern()),
        "MATCH ( ) RETURN foo",
        dict(),
    ),
])
def test_read(reading_clause, query, parameters):
    ast = Cypher(
        statement=SinglePartReadQuery(
            return_=Return(
                body=ReturnBody(
                    items=NonEmptyList[ReturnItem](
                        Expression("foo"),
                    ),
                ),
            ),
            reading_clauses=[
                reading_clause,
            ] if reading_clause else [],
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


@parameterized([
    (
        "foo", Match(pattern=NodePattern()),
        "MATCH ( ) MERGE ( ) RETURN foo",
        dict(),
    ),
    (
        "foo", None,
        "MERGE ( ) RETURN foo",
        dict(),
    ),
    (
        None, Match(pattern=NodePattern()),
        "MATCH ( ) MERGE ( )",
        dict(),
    ),
    (
        None, None,
        "MERGE ( )",
        dict(),
    ),
])
def test_write(value, reading_clause, query, parameters):
    ast = Cypher(
        statement=SinglePartWriteQuery(
            return_=Return(
                body=ReturnBody(
                    items=NonEmptyList[ReturnItem](
                        Expression(value),
                    ),
                ),
            ) if value else None,
            reading_clauses=[
                reading_clause,
            ] if reading_clause else [],
            updating_clauses=[
                Merge(pattern_part=PatternPart()),
            ],
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
