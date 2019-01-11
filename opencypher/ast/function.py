from dataclasses import dataclass
from typing import Iterable

from opencypher.ast.expression import Expression
from opencypher.ast.parameter import Parameter, Parameterized
from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import FunctionName


@dataclass(frozen=True)
class FunctionInvocation(Parameterized):
    """
    FunctionInvocation = FunctionName, [SP], '(', [SP], [(D,I,S,T,I,N,C,T), [SP]], [Expression, [SP], { ',', [SP], Expression, [SP] }], ')' ;  # noqa: E501

    """
    name: FunctionName
    expressions: NonEmptySequence[Expression]
    distinct: bool = False

    def __str__(self) -> str:
        if self.distinct:
            return f"{self.name}(DISTINCT {str_join(self.expressions)})"
        else:
            return f"{self.name}({str_join(self.expressions)})"

    def iter_parameters(self) -> Iterable[Parameter]:
        if self.expressions:
            for expression in self.expressions:
                yield from expression.iter_parameters()
