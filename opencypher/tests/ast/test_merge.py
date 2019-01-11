from hamcrest import assert_that, equal_to, is_
from parameterized import parameterized

from opencypher.ast import (
    Expression,
    Merge,
    MergeAction,
    MergeActionType,
    PatternPart,
    Set,
    SetItems,
    SetVariableItem,
)


@parameterized([
    (
        None,
        "MERGE ()",
        dict(),
    ),
    (
        [
            MergeActionType.CREATE,
        ],
        "MERGE () ON CREATE SET foo = bar",
        dict(),
    ),
    (
        [
            MergeActionType.MATCH,
        ],
        "MERGE () ON MATCH SET foo = bar",
        dict(),
    ),
    (
        [
            MergeActionType.CREATE,
            MergeActionType.MATCH,
        ],
        "MERGE () ON CREATE SET foo = bar ON MATCH SET foo = bar",
        dict(),
    ),
])
def test_merge(action_types, query, parameters):
    ast = Merge(
        pattern_part=PatternPart(),
        actions=[
            MergeAction(
                action_type=action_type,
                then=Set(
                    items=SetItems(
                        SetVariableItem(
                            target="foo",
                            value=Expression("bar"),
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
