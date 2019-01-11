from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    Cypher,
    Expression,
    Match,
    Merge,
    NodePattern,
    NonEmptySequence,
    Pattern,
    PatternElement,
    PatternPart,
    SinglePartReadQuery,
    SinglePartWriteQuery,
    RegularQuery,
    Return,
    ReturnBody,
    ReturnItem,
    Union,
)


MATCH = Match(
    Pattern(
        items=NonEmptySequence[PatternPart](
            PatternPart(
                PatternElement(
                    NodePattern(),
                ),
            ),
        ),
    ),
)


@parameterized([
    (
        None,
        "RETURN foo",
        dict(),
    ),
    (
        MATCH,
        "MATCH () RETURN foo",
        dict(),
    ),
])
def test_read(reading_clause, query, parameters):
    ast = Cypher(
        statement=RegularQuery(
            query=SinglePartReadQuery(
                return_=Return(
                    body=ReturnBody(
                        items=NonEmptySequence[ReturnItem](
                            Expression("foo"),
                        ),
                    ),
                ),
                reading_clauses=[
                    reading_clause,
                ] if reading_clause else [],
            ),
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
        "foo", MATCH,
        "MATCH () MERGE () RETURN foo",
        dict(),
    ),
    (
        "foo", None,
        "MERGE () RETURN foo",
        dict(),
    ),
    (
        None, MATCH,
        "MATCH () MERGE ()",
        dict(),
    ),
    (
        None, None,
        "MERGE ()",
        dict(),
    ),
])
def test_write(value, reading_clause, query, parameters):
    ast = Cypher(
        statement=RegularQuery(
            query=SinglePartWriteQuery(
                return_=Return(
                    body=ReturnBody(
                        items=NonEmptySequence[ReturnItem](
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
        ["foo", "bar"],
        False,
        "RETURN foo UNION RETURN bar",
        dict()
    ),
    (
        ["foo", "bar", "baz"],
        True,
        "RETURN foo UNION ALL RETURN bar UNION ALL RETURN baz",
        dict()
    ),
])
def test_union(values, all, query, parameters):
    queries = [
        SinglePartReadQuery(
            return_=Return(
                body=ReturnBody(
                    items=NonEmptySequence[ReturnItem](
                        Expression(value),
                    ),
                ),
            ),
        )
        for value in values
    ]
    ast = Cypher(
        statement=RegularQuery(
            query=queries[0],
            items=NonEmptySequence[Union](
                *(
                    Union(
                        query=query,
                        all=all,
                    )
                    for query in queries[1:]
                )
            ),
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
