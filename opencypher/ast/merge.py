from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Iterable, List

from opencypher.ast.expression import Parameter, Parameterized
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
class MergeAction(Parameterized):
    action_type: MergeActionType
    then: Set

    def __str__(self) -> str:
        return f"ON {str(self.action_type)} {str(self.then)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.then.iter_parameters()


@dataclass(frozen=True)
class Merge(Parameterized):
    pattern_part: PatternPart
    actions: List[MergeAction] = field(default_factory=list)

    def __str__(self) -> str:
        if self.actions:
            return f"MERGE {str(self.pattern_part)} {stringify(self.actions)}"
        else:
            return f"MERGE {str(self.pattern_part)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.pattern_part.iter_parameters()
        for action in self.actions:
            yield from action.iter_parameters()
