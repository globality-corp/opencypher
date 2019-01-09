from typing import Iterable, List, Tuple, Union

from opencypher.ast.expression import Expression, Parameter
from opencypher.ast.values import PropertyKeyName


def stringify(item: Tuple[PropertyKeyName, Expression]) -> str:
    key, value = item
    return f"{str(key)}: {str(value)}"


class MapLiteral(List[Tuple[PropertyKeyName, Expression]]):

    def __str__(self) -> str:
        return f"""{{ {", ".join(stringify(item) for item in self)} }}"""

    def iter_parameters(self) -> Iterable[Parameter]:
        for key, value in self:
            yield from value.iter_parameters()


Properties = Union[
    MapLiteral,
    Parameter,
]
