from dataclasses import dataclass
from typing import Iterable, Optional

from opencypher.ast.expression import Expression, Parameter
from opencypher.ast.pattern import Pattern


@dataclass(frozen=True)
class Where:
    expression: Expression

    def __str__(self) -> str:
        return f"WHERE {str(self.expression)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.expression.iter_parameters()


@dataclass(frozen=True)
class Match:
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
