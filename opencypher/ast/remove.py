from dataclasses import dataclass
from typing import Iterable, Tuple, Union

from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import NodeLabels, Variable
from opencypher.ast.parameter import Parameter, Parameterized
from opencypher.ast.properties import PropertyExpression


@dataclass
class RemoveItem(Parameterized):
    """
    RemoveItem = (Variable, NodeLabels)
               | PropertyExpression

    """
    value: Union[Tuple[Variable, NodeLabels], PropertyExpression]

    def __str__(self) -> str:
        if isinstance(self.value, PropertyExpression):
            return str(self.value)
        else:
            return f"{str(self.value[0])}{str_join(self.value[1], '')}"

    def iter_parameters(self) -> Iterable[Parameter]:
        if isinstance(self.value, PropertyExpression):
            yield from self.value.iter_parameters()


RemoveItems = NonEmptySequence[RemoveItem]


@dataclass(frozen=True)
class Remove(Parameterized):
    """
    Remove = (R,E,M,O,V,E), SP, RemoveItem, { [SP], ',', [SP], RemoveItem } ;

    """
    items: RemoveItems

    def __str__(self) -> str:
        return f"REMOVE {str_join(self.items, ',')}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for item in self.items:
            yield from item.iter_parameters()
