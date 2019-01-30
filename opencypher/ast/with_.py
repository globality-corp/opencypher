from dataclasses import dataclass
from typing import Iterable, Optional

from opencypher.ast.match import Where
from opencypher.ast.parameter import Parameter, Parameterized
from opencypher.ast.return_ import ReturnBody


@dataclass(frozen=True)
class With(Parameterized):
    """
    With = (W,I,T,H), [[SP], (D,I,S,T,I,N,C,T)], SP, ReturnBody, [[SP], Where] ;

    """
    body: ReturnBody
    distinct: bool = False
    where: Optional[Where] = None

    def __str__(self) -> str:
        if self.distinct:
            if self.where is not None:
                return f"WITH DISTINCT {str(self.body)} {str(self.where)}"
            else:
                return f"WITH DISTINCT {str(self.body)}"
        else:
            if self.where is not None:
                return f"WITH {str(self.body)} {str(self.where)}"
            else:
                return f"WITH {str(self.body)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        if self.where is not None:
            yield from self.where.iter_parameters()
