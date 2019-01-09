from dataclasses import dataclass
from typing import Iterable, Iterator, Tuple, Union

from opencypher.ast.nonemptylist import stringify, NonEmptyList
from opencypher.ast.values import (
    FunctionName,
    PropertyKeyName,
    SymbolicName,
    Variable,
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
    # omitted: DecimialInteger
    key: PropertyKeyName
    name: SymbolicName
    value: str

    def __str__(self) -> str:
        return f"${str(self.name)}"

    def iter_parameters(self) -> Iterable["Parameter"]:
        yield self


@dataclass(frozen=True)
class FunctionInvocation(Parameterized):
    name: FunctionName
    expressions: NonEmptyList["Expression"]
    distinct: bool = False

    def __str__(self) -> str:
        if self.distinct:
            return f"{self.name}( DISTINCT {stringify(self.expressions)} )"
        else:
            return f"{self.name}( {stringify(self.expressions)} )"


# omitting many things here
Literal = Union[
    bool,
    float,
    int,
    str,
]

# omitting many things here
Atom = Union[
    Literal,
    FunctionInvocation,
    Parameter,
]


@dataclass(frozen=True)
class Expression(Parameterized):
    # omitting many things here
    value: Atom

    def __str__(self) -> str:
        return str(self.value)

    def iter_parameters(self) -> Iterable[Parameter]:
        if isinstance(self.value, FunctionInvocation):
            for expression in self.value.expressions:
                yield from expression.iter_parameters()
        elif isinstance(self.value, Parameter):
            yield from self.value.iter_parameters()


@dataclass
class ExpressionAlias(Parameterized):
    expression: Expression
    variable: Variable

    def __str__(self) -> str:
        return f"{str(self.expression)} AS {str(self.variable)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.expression.iter_parameters()
