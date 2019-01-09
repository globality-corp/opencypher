from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Iterable, List

from opencypher.ast.expression import Parameter
from opencypher.ast.nonemptylist import stringify
from opencypher.ast.pattern import PatternPart
from opencypher.ast.set import Set


@unique
class MergeActionType(Enum):
    CREATE = "CREATE"
    MATCH = "MATCH"

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class MergeAction:
    merge_action_type: MergeActionType
    set_clause: Set

    def __str__(self) -> str:
        return f"ON {str(self.merge_action_type)} {str(self.set_clause)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.set_clause.iter_parameters()


@dataclass(frozen=True)
class Merge:
    pattern_part: PatternPart
    merge_actions: List[MergeAction] = field(default_factory=list)

    def __str__(self) -> str:
        if self.merge_actions:
            return f"MERGE {str(self.pattern_part)} {stringify(self.merge_actions)}"
        else:
            return f"MERGE {str(self.pattern_part)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.pattern_part.iter_parameters()
        for merge_action in self.merge_actions:
            yield from merge_action.iter_parameters()
