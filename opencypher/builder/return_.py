from typing import Optional

from opencypher.ast import (
    NonEmptyList,
    Limit,
    Order,
    Skip,
    Return,
    ReturnBody,
    ReturnItem,
    SortItem,
    SortOrder,
)
from opencypher.builder import expr


class ReturnFactory:

    @classmethod
    def order(cls, item: str, *items: str, order: Optional[SortOrder] = None) -> Order:
        return Order(
            items=NonEmptyList[SortItem](
                SortItem(
                    expression=expr(item),
                    order=order,
                ),
            ),
        )

    @classmethod
    def asc(cls, item: str, *items: str) -> Order:
        return cls.order(item, *items, order=SortOrder.ASCENDING)

    @classmethod
    def desc(cls, item: str, *items: str) -> Order:
        return cls.order(item, *items, order=SortOrder.DESCENDING)

    @classmethod
    def ret(cls,
            item: ReturnItem,
            *items: ReturnItem,
            order: Optional[Order] = None,
            skip: Optional[int] = None,
            limit: Optional[int] = None) -> Return:
        return Return(
            body=ReturnBody(
                items=NonEmptyList[ReturnItem](
                    item,
                    *(
                        arg
                        for arg in items
                    ),
                ),
                order=order,
                skip=Skip(expr(skip)) if skip is not None else None,
                limit=Limit(expr(limit)) if limit is not None else None,
            ),
        )


asc = ReturnFactory.asc
desc = ReturnFactory.desc
