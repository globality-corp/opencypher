from dataclasses import dataclass
from typing import Iterable

from opencypher.ast.expression import Expression, Parameter
from opencypher.ast.nonemptylist import stringify, NonEmptyList
from opencypher.ast.values import Variable


@dataclass(frozen=True)
class SetItem:
    # omitted: PropertyExpression
    variable: Variable
    # omitted: = vs +=
    expression: Expression
    # omitted: NonEmptyList[NodeLabel]

    def __str__(self) -> str:
        return f"{str(self.variable)} = {str(self.expression)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.expression.iter_parameters()


@dataclass(frozen=True)
class Set:
    items: NonEmptyList[SetItem]

    def __str__(self) -> str:
        return f"SET {stringify(self.items, ', ')}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for item in self.items:
            yield from item.iter_parameters()
