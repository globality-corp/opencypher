from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    Expression,
    Merge,
    MergeAction,
    MergeActionType,
    NonEmptySequence,
    PatternPart,
    Set,
    SetItem,
)


@parameterized([
    (
        None,
        "MERGE ( )",
        dict(),
    ),
    (
        [
            MergeActionType.CREATE,
        ],
        "MERGE ( ) ON CREATE SET foo = bar",
        dict(),
    ),
    (
        [
            MergeActionType.MATCH,
        ],
        "MERGE ( ) ON MATCH SET foo = bar",
        dict(),
    ),
    (
        [
            MergeActionType.CREATE,
            MergeActionType.MATCH,
        ],
        "MERGE ( ) ON CREATE SET foo = bar ON MATCH SET foo = bar",
        dict(),
    ),
])
def test_match(action_types, query, parameters):
    ast = Merge(
        pattern_part=PatternPart(),
        actions=[
            MergeAction(
                action_type=action_type,
                then=Set(
                    items=NonEmptySequence[SetItem](
                        SetItem(
                            variable="foo",
                            expression=Expression("bar"),
                        ),
                    ),
                ),
            )
            for action_type in action_types or []
        ]
    )
    assert_that(
        str(ast),
        is_(equal_to(query)),
    )
    assert_that(
        dict(ast),
        is_(equal_to(parameters)),
    )
