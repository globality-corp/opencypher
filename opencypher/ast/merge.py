from dataclasses import dataclass
from enum import Enum, unique
from typing import Iterable, Optional, Sequence

from opencypher.ast.formatting import str_join
from opencypher.ast.parameter import Parameter, Parameterized
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
    """
    MergeAction = ((O,N), SP, (M,A,T,C,H), SP, Set)
                | ((O,N), SP, (C,R,E,A,T,E), SP, Set)
                ;

    """
    action_type: MergeActionType
    then: Set

    def __str__(self) -> str:
        return f"ON {str(self.action_type)} {str(self.then)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.then.iter_parameters()


@dataclass(frozen=True)
class Merge(Parameterized):
    """
    Merge = (M,E,R,G,E), [SP], PatternPart, { SP, MergeAction } ;

    """
    pattern_part: PatternPart
    actions: Optional[Sequence[MergeAction]] = None

    def __str__(self) -> str:
        if self.actions:
            return f"MERGE {str(self.pattern_part)} {str_join(self.actions)}"
        else:
            return f"MERGE {str(self.pattern_part)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.pattern_part.iter_parameters()
        if self.actions:
            for action in self.actions:
                yield from action.iter_parameters()
