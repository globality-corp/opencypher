from dataclasses import dataclass
from typing import Iterable

from opencypher.ast.expression import Expression, Parameter
from opencypher.ast.nonemptylist import stringify, NonEmptyList


@dataclass(frozen=True)
class Delete:
    items: NonEmptyList[Expression]
    detach: bool = False

    def __str__(self) -> str:
        if self.detach:
            return f"DETACH DELETE {stringify(self.items, ', ')}"
        else:
            return f"DELETE {stringify(self.items, ', ')}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for item in self.items:
            yield from item.iter_parameters()
