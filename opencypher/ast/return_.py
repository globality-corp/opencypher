from dataclasses import dataclass
from typing import Optional, Union

from opencypher.ast.expression import Expression, ExpressionAlias
from opencypher.ast.paging import Limit, Skip
from opencypher.ast.nonemptylist import stringify, NonEmptyList
from opencypher.ast.sorting import Order


ReturnItem = Union[
    Expression,
    ExpressionAlias,
]


@dataclass(frozen=True)
class ReturnBody:
    items: NonEmptyList[ReturnItem]
    order: Optional[Order] = None
    skip: Optional[Skip] = None
    limit: Optional[Limit] = None

    def __str__(self) -> str:
        if self.order is not None:
            if self.skip is not None:
                if self.limit is not None:
                    return f"{stringify(self.items, ', ')} {str(self.order)} {str(self.skip)} {str(self.limit)}"
                else:
                    return f"{stringify(self.items, ', ')} {str(self.order)} {str(self.skip)}"
            else:
                if self.limit is not None:
                    return f"{stringify(self.items, ', ')} {str(self.order)} {str(self.limit)}"
                else:
                    return f"{stringify(self.items, ', ')} {str(self.order)}"
        else:
            if self.skip is not None:
                if self.limit is not None:
                    return f"{stringify(self.items, ', ')} {str(self.skip)} {str(self.limit)}"
                else:
                    return f"{stringify(self.items, ', ')} {str(self.skip)}"
            else:
                if self.limit is not None:
                    return f"{stringify(self.items, ', ')} {str(self.limit)}"
                else:
                    return f"{stringify(self.items, ', ')}"


@dataclass(frozen=True)
class Return:
    body: ReturnBody
    distinct: bool = False

    def __str__(self) -> str:
        if self.distinct:
            return f"RETURN DISTINCT {str(self.body)}"
        else:
            return f"RETURN {str(self.body)}"
