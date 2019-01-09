from dataclasses import dataclass
from typing import Iterable, Optional

from opencypher.ast.expression import Parameter, Parameterized
from opencypher.ast.nonemptylist import stringify, NonEmptyList
from opencypher.ast.properties import Properties
from opencypher.ast.values import NodeLabel, Variable


@dataclass(frozen=True)
class NodePattern(Parameterized):
    variable: Optional[Variable] = None
    labels: Optional[NonEmptyList[NodeLabel]] = None
    properties: Optional[Properties] = None

    def __str__(self) -> str:
        if self.variable is not None:
            if self.labels is not None:
                if self.properties is not None:
                    return f"( {str(self.variable)} {stringify(self.labels)} {str(self.properties)} )"
                else:
                    return f"( {str(self.variable)} {stringify(self.labels)} )"
            else:
                if self.properties is not None:
                    return f"( {str(self.variable)} {str(self.properties)} )"
                else:
                    return f"( {str(self.variable)} )"
        else:
            if self.labels is not None:
                if self.properties is not None:
                    return f"( {stringify(self.labels)} {str(self.properties)} )"
                else:
                    return f"( {stringify(self.labels)} )"
            else:
                if self.properties is not None:
                    return f"( {str(self.properties)} )"
                else:
                    return f"( )"

    def iter_parameters(self) -> Iterable[Parameter]:
        if self.properties is not None:
            yield from self.properties.iter_parameters()
