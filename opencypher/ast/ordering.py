from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional

from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.expression import Expression
from opencypher.ast.formatting import str_join


@unique
class SortOrder(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class SortItem:
    """
    SortItem = Expression, [[SP], ((A,S,C,E,N,D,I,N,G) | (A,S,C) | (D,E,S,C,E,N,D,I,N,G) | (D,E,S,C))] ;

    """
    expression: Expression
    order: Optional[SortOrder] = None

    def __str__(self) -> str:
        if self.order is not None:
            return f"{str(self.expression)} {str(self.order)}"
        else:
            return f"{str(self.expression)}"


@dataclass(frozen=True)
class Order:
    """
    Order = (O,R,D,E,R), SP, (B,Y), SP, SortItem, { ',', [SP], SortItem } ;

    """
    items: NonEmptySequence[SortItem]

    def __str__(self) -> str:
        return f"ORDER BY {str_join(self.items, ', ')}"
