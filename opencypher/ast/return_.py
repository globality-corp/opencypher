from dataclasses import dataclass
from typing import Iterable, Optional, Union

from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.expression import Expression
from opencypher.ast.formatting import str_join
from opencypher.ast.ordering import Order
from opencypher.ast.paging import Limit, Skip
from opencypher.ast.parameter import Parameter, Parameterized
from opencypher.ast.naming import Variable


@dataclass(frozen=True)
class ExpressionAlias(Parameterized):
    """
    ReturnItem = (Expression, SP, (A,S), SP, Variable)
               | ...
               ;
    """
    expression: Expression
    variable: Variable

    def __str__(self) -> str:
        return f"{str(self.expression)} AS {str(self.variable)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.expression.iter_parameters()


"""
ReturnItem = (Expression, SP, (A,S), SP, Variable)
           | Expression
           ;

"""
ReturnItem = Union[
    Expression,
    ExpressionAlias,
]


"""
ReturnItems = ('*', { [SP], ',', [SP], ReturnItem })
            | (ReturnItem, { [SP], ',', [SP], ReturnItem })
            ;
"""
# omitted: explicit wildcard support; as of this writing the Expression grammar is sufficiently
# permissive to allow '*' to be passed as an expression.
ReturnItems = NonEmptySequence[ReturnItem]


@dataclass(frozen=True)
class ReturnBody:
    """
    ReturnBody = ReturnItems, [SP, Order], [SP, Skip], [SP, Limit] ;

    """
    items: ReturnItems
    order: Optional[Order] = None
    skip: Optional[Skip] = None
    limit: Optional[Limit] = None

    def __str__(self) -> str:
        if self.order is not None:
            if self.skip is not None:
                if self.limit is not None:
                    return f"{str_join(self.items, ', ')} {str(self.order)} {str(self.skip)} {str(self.limit)}"
                else:
                    return f"{str_join(self.items, ', ')} {str(self.order)} {str(self.skip)}"
            else:
                if self.limit is not None:
                    return f"{str_join(self.items, ', ')} {str(self.order)} {str(self.limit)}"
                else:
                    return f"{str_join(self.items, ', ')} {str(self.order)}"
        else:
            if self.skip is not None:
                if self.limit is not None:
                    return f"{str_join(self.items, ', ')} {str(self.skip)} {str(self.limit)}"
                else:
                    return f"{str_join(self.items, ', ')} {str(self.skip)}"
            else:
                if self.limit is not None:
                    return f"{str_join(self.items, ', ')} {str(self.limit)}"
                else:
                    return f"{str_join(self.items, ', ')}"


@dataclass(frozen=True)
class Return:
    """
    Return = (R,E,T,U,R,N), [[SP], (D,I,S,T,I,N,C,T)], SP, ReturnBody ;

    """
    body: ReturnBody
    distinct: bool = False

    def __str__(self) -> str:
        if self.distinct:
            return f"RETURN DISTINCT {str(self.body)}"
        else:
            return f"RETURN {str(self.body)}"
