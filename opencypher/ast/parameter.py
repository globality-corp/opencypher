from dataclasses import dataclass
from typing import Iterable, Iterator, Tuple

from opencypher.ast.naming import (
    PropertyKeyName,
    SymbolicName,
)


class Parameterized:
    """
    A mixin for an object that has zero or more `Parameter`.

    """
    def __iter__(self) -> Iterator[Tuple[str, str]]:
        """
        Expose parameters as an iterable such that `dict(self)` can be passed to the driver
        as a parameter dictionary.

        """
        return iter(
            (parameter.name, parameter.value)
            for parameter in self.iter_parameters()
        )

    def iter_parameters(self) -> Iterable["Parameter"]:
        """
        Iterate over available parameters.

        """
        return ()


@dataclass(frozen=True)
class Parameter(Parameterized):
    """
    Parameter = '$', (SymbolicName | DecimalInteger) ;

    Keeps additional state for ease of producing bound query parameters.

    """
    # omitted: DecimialInteger
    key: PropertyKeyName
    name: SymbolicName
    value: str

    def __str__(self) -> str:
        return f"${str(self.name)}"

    def iter_parameters(self) -> Iterable["Parameter"]:
        yield self
