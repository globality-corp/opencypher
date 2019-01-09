from dataclasses import dataclass
from typing import Iterable

from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.expression import Expression, Parameter
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import Variable


@dataclass(frozen=True)
class SetItem:
    """
    SetItem = (PropertyExpression, [SP], '=', [SP], Expression)
        | (Variable, [SP], '=', [SP], Expression)
        | (Variable, [SP], '+=', [SP], Expression)
        | (Variable, [SP], NodeLabels)
        ;

    """
    # omitted: PropertyExpression
    variable: Variable
    # omitted: +=
    expression: Expression
    # omitted: NodeLabels

    def __str__(self) -> str:
        return f"{str(self.variable)} = {str(self.expression)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.expression.iter_parameters()


@dataclass(frozen=True)
class Set:
    """
    Set = (S,E,T), [SP], SetItem, { ',', SetItem } ;

    """
    items: NonEmptySequence[SetItem]

    def __str__(self) -> str:
        return f"SET {str_join(self.items, ', ')}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for item in self.items:
            yield from item.iter_parameters()
