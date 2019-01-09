from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional

from opencypher.ast.expression import Expression
from opencypher.ast.nonemptylist import stringify, NonEmptyList


@unique
class SortOrder(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class SortItem:
    expression: Expression
    order: Optional[SortOrder]

    def __str__(self) -> str:
        if self.order is not None:
            return f"{str(self.expression)} {str(self.order)}"
        else:
            return f"{str(self.expression)}"


@dataclass(frozen=True)
class Order:
    items: NonEmptyList[SortItem]

    def __str__(self) -> str:
        return f"ORDER BY {stringify(self.items, ', ')}"
