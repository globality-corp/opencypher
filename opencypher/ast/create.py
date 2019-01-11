from dataclasses import dataclass
from typing import Iterable

from opencypher.ast.parameter import Parameter, Parameterized
from opencypher.ast.pattern import Pattern


@dataclass(frozen=True)
class Create(Parameterized):
    """
    Create = (C,R,E,A,T,E), [SP], Pattern ;

    """
    pattern: Pattern

    def __str__(self) -> str:
        return f"CREATE {str(self.pattern)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.pattern.iter_parameters()
