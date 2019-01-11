from dataclasses import dataclass
from typing import Iterable, Optional

from opencypher.ast.expression import Parameter, Parameterized
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import NodeLabels, Variable
from opencypher.ast.properties import Properties


@dataclass(frozen=True)
class NodePattern(Parameterized):
    """
    NodePattern = '(', [SP], [Variable, [SP]], [NodeLabels, [SP]], [Properties, [SP]], ')' ;

    """
    variable: Optional[Variable] = None
    labels: Optional[NodeLabels] = None
    properties: Optional[Properties] = None

    def __str__(self) -> str:
        if self.variable is not None:
            if self.labels is not None:
                if self.properties is not None:
                    return f"({str(self.variable)}{str_join(self.labels, '')} {str(self.properties)})"
                else:
                    return f"({str(self.variable)}{str_join(self.labels, '')})"
            else:
                if self.properties is not None:
                    return f"({str(self.variable)} {str(self.properties)})"
                else:
                    return f"({str(self.variable)})"
        else:
            if self.labels is not None:
                if self.properties is not None:
                    return f"({str_join(self.labels, '')} {str(self.properties)})"
                else:
                    return f"({str_join(self.labels, '')})"
            else:
                if self.properties is not None:
                    return f"({str(self.properties)})"
                else:
                    return f"()"

    def iter_parameters(self) -> Iterable[Parameter]:
        if self.properties is not None:
            yield from self.properties.iter_parameters()
