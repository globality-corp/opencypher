from dataclasses import dataclass
from typing import Iterable

from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.expression import Expression
from opencypher.ast.formatting import str_join
from opencypher.ast.parameter import Parameter, Parameterized


@dataclass(frozen=True)
class Delete(Parameterized):
    """
    Delete = [(D,E,T,A,C,H), SP], (D,E,L,E,T,E), [SP], Expression, { [SP], ',', [SP], Expression } ;

    """
    items: NonEmptySequence[Expression]
    detach: bool = False

    def __str__(self) -> str:
        if self.detach:
            return f"DETACH DELETE {str_join(self.items, ', ')}"
        else:
            return f"DELETE {str_join(self.items, ', ')}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for item in self.items:
            yield from item.iter_parameters()
