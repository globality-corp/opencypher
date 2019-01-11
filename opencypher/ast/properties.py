from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple, Union

from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.expression import Atom, Expression
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import PropertyKeyName
from opencypher.ast.parameter import Parameter, Parameterized


@dataclass(frozen=True)
class PropertyLookup:
    """
    PropertyLookup = . PropertyKeyName

    """
    value: PropertyKeyName

    def __str__(self) -> str:
        return f".{self.value}"


@dataclass(frozen=True)
class PropertyExpression(Parameterized):
    """
    PropertyExpression = Atom PropertyLookup+

    """
    value: Atom
    properties: NonEmptySequence[PropertyLookup]

    def __str__(self) -> str:
        return f"{self.value}{str_join(self.properties, '')}"

    def iter_parameters(self) -> Iterable[Parameter]:
        if isinstance(self.value, Parameter):
            yield from self.value.iter_parameters()


@dataclass(frozen=True)
class MapLiteral(Parameterized):
    """
    MapLiteral = '{', [SP], [PropertyKeyName, [SP], ':', [SP], Expression, [SP], { ',', [SP], PropertyKeyName, [SP], ':', [SP], Expression, [SP] }], '}' ;  # noqa: E501

    """
    items: Sequence[Tuple[PropertyKeyName, Expression]]

    def __str__(self) -> str:
        items = (
            f"{str(key)}: {str(value)}"
            for key, value in self.items
        )
        return f"{{{str_join(items, ', ')}}}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for key, value in self.items:
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
