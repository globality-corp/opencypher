from dataclasses import dataclass
from typing import Iterable

from opencypher.ast.expression import Expression
from opencypher.ast.naming import Variable
from opencypher.ast.parameter import Parameter, Parameterized


@dataclass(frozen=True)
class Unwind(Parameterized):
    """
    Unwind = (U,N,W,I,N,D), [SP], Expression, SP, (A,S), SP, Variable ;

    """
    expression: Expression
    variable: Variable

    def __str__(self) -> str:
        return f"UNWIND {str(self.expression)} AS {str(self.variable)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.expression.iter_parameters()
