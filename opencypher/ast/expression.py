from dataclasses import dataclass
from typing import Iterable, Union

from opencypher.ast.nonemptylist import stringify, NonEmptyList
from opencypher.ast.values import (
    FunctionName,
    PropertyKeyName,
    SymbolicName,
    Variable,
)


@dataclass(frozen=True)
class Parameter:
    # omitted: DecimialInteger
    key: PropertyKeyName
    name: SymbolicName
    value: str

    def __str__(self) -> str:
        return f"${str(self.name)}"

    def iter_parameters(self) -> Iterable["Parameter"]:
        yield self


@dataclass(frozen=True)
class FunctionInvocation:
    name: FunctionName
    expressions: NonEmptyList["Expression"]
    distinct: bool = False

    def __str__(self) -> str:
        if self.distinct:
            return f"{self.name}( DISTINCT {str(self.expressions)} )"
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
class Expression:
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
class ExpressionAlias:
    expression: Expression
    variable: Variable

    def __str__(self) -> str:
        return f"{str(self.expression)} AS {str(self.variable)}"
