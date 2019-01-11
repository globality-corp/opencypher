from dataclasses import dataclass
from typing import Iterable, Optional

from opencypher.ast.expression import Expression
from opencypher.ast.parameter import Parameter, Parameterized
from opencypher.ast.pattern import Pattern


@dataclass(frozen=True)
class Where(Parameterized):
    """
    Where = (W,H,E,R,E), SP, Expression ;

    """
    expression: Expression

    def __str__(self) -> str:
        return f"WHERE {str(self.expression)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.expression.iter_parameters()


@dataclass(frozen=True)
class Match(Parameterized):
    """
    Match = [(O,P,T,I,O,N,A,L), SP], (M,A,T,C,H), [SP], Pattern, [[SP], Where] ;

    """
    pattern: Pattern
    optional: bool = False
    where: Optional[Where] = None

    def __str__(self) -> str:
        if self.optional:
            if self.where:
                return f"OPTIONAL MATCH {str(self.pattern)} {str(self.where)}"
            else:
                return f"OPTIONAL MATCH {str(self.pattern)}"
        else:
            if self.where:
                return f"MATCH {str(self.pattern)} {str(self.where)}"
            else:
                return f"MATCH {str(self.pattern)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.pattern.iter_parameters()
        if self.where is not None:
            yield from self.where.iter_parameters()
