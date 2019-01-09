from typing import Iterable, Tuple, Union

from opencypher.ast.expression import Expression, Parameter
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import PropertyKeyName


class MapLiteral(Tuple[Tuple[PropertyKeyName, Expression]]):
    """
    MapLiteral = '{', [SP], [PropertyKeyName, [SP], ':', [SP], Expression, [SP], { ',', [SP], PropertyKeyName, [SP], ':', [SP], Expression, [SP] }], '}' ;  # noqa: E501

    """
    def __str__(self) -> str:
        items = (
            f"{str(key)}: {str(value)}"
            for key, value in self
        )
        return f"{{ {str_join(items, ', ')} }}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for key, value in self:
            yield from value.iter_parameters()


"""
Properties = MapLiteral
           | Parameter
           ;

"""
Properties = Union[
    MapLiteral,
    Parameter,
]
