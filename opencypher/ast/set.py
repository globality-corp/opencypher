from dataclasses import dataclass
from typing import Iterable, Union

from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.expression import Expression
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import NodeLabels, Variable
from opencypher.ast.parameter import Parameter, Parameterized
from opencypher.ast.properties import PropertyExpression


@dataclass(frozen=True)
class SetPropertyItem(Parameterized):
    """
    (PropertyExpression, [SP], '=', [SP], Expression)

    """
    target: PropertyExpression
    value: Expression

    def __str__(self) -> str:
        return f"{str(self.target)} = {str(self.value)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.target.iter_parameters()
        yield from self.value.iter_parameters()


@dataclass(frozen=True)
class SetVariableItem(Parameterized):
    """
    (Variable, [SP], '=', [SP], Expression) | (Variable, [SP], '+=', [SP], Expression)

    """
    target: Variable
    value: Expression
    mutate: bool = False

    def __str__(self) -> str:
        if self.mutate:
            return f"{str(self.target)} += {str(self.value)}"
        else:
            return f"{str(self.target)} = {str(self.value)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.value.iter_parameters()


@dataclass(frozen=True)
class SetVariableNodeLabelsItem(Parameterized):
    """
    (Variable, [SP], NodeLabels)

    """
    target: Variable
    value: NodeLabels

    def __str__(self) -> str:
        return f"{str(self.target)}{str_join(self.value, '')}"

    def iter_parameters(self) -> Iterable[Parameter]:
        return []


"""
SetItem = (PropertyExpression, [SP], '=', [SP], Expression)
        | (Variable, [SP], '=', [SP], Expression)
        | (Variable, [SP], '+=', [SP], Expression)
        | (Variable, [SP], NodeLabels)
        ;
"""
SetItem = Union[
    SetPropertyItem,
    SetVariableItem,
    SetVariableNodeLabelsItem,
]

SetItems = NonEmptySequence[SetItem]


@dataclass(frozen=True)
class Set(Parameterized):
    """
    Set = (S,E,T), [SP], SetItem, { ',', SetItem } ;

    """
    items: SetItems

    def __str__(self) -> str:
        return f"SET {str_join(self.items, ', ')}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for item in self.items:
            yield from item.iter_parameters()
