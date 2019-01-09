from dataclasses import dataclass
from typing import Iterable, Iterator, Tuple, Union

from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.formatting import str_join
from opencypher.ast.naming import (
    FunctionName,
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


@dataclass(frozen=True)
class FunctionInvocation(Parameterized):
    """
    FunctionInvocation = FunctionName, [SP], '(', [SP], [(D,I,S,T,I,N,C,T), [SP]], [Expression, [SP], { ',', [SP], Expression, [SP] }], ')' ;  # noqa: E501

    """
    name: FunctionName
    expressions: NonEmptySequence["Expression"]
    distinct: bool = False

    def __str__(self) -> str:
        if self.distinct:
            return f"{self.name}( DISTINCT {str_join(self.expressions)} )"
        else:
            return f"{self.name}( {str_join(self.expressions)} )"


"""
Literal = NumberLiteral
        | StringLiteral
        | BooleanLiteral
        | (N,U,L,L)
        | MapLiteral
        | ListLiteral
        ;
"""
# omitting many things here
Literal = Union[
    bool,
    float,
    int,
    str,
]

"""
Atom = Literal
     | Parameter
     | CaseExpression
     | ((C,O,U,N,T), [SP], '(', [SP], '*', [SP], ')')
     | ListComprehension
     | PatternComprehension
     | ((A,L,L), [SP], '(', [SP], FilterExpression, [SP], ')')
     | ((A,N,Y), [SP], '(', [SP], FilterExpression, [SP], ')')
     | ((N,O,N,E), [SP], '(', [SP], FilterExpression, [SP], ')')
     | ((S,I,N,G,L,E), [SP], '(', [SP], FilterExpression, [SP], ')')
     | RelationshipsPattern
     | ParenthesizedExpression
     | FunctionInvocation
     | Variable
     ;
"""
# omitting many things here
Atom = Union[
    Literal,
    FunctionInvocation,
    Parameter,
]


@dataclass(frozen=True)
class Expression(Parameterized):
    """
    Expression = OrExpression ;
    OrExpression = XorExpression, { SP, (O,R), SP, XorExpression } ;
    XorExpression = AndExpression, { SP, (X,O,R), SP, AndExpression } ;
    AndExpression = NotExpression, { SP, (A,N,D), SP, NotExpression } ;
    NotExpression = { (N,O,T), [SP] }, ComparisonExpression ;
    ComparisonExpression = AddOrSubtractExpression, { [SP], PartialComparisonExpression } ;
    AddOrSubtractExpression = MultiplyDivideModuloExpression, { ([SP], '+', [SP], MultiplyDivideModuloExpression) | ([SP], '-', [SP], MultiplyDivideModuloExpression) } ;  # noqa: E501
    MultiplyDivideModuloExpression = PowerOfExpression, { ([SP], '*', [SP], PowerOfExpression) | ([SP], '/', [SP], PowerOfExpression) | ([SP], '%', [SP], PowerOfExpression) } ;  # noqa: E501
    PowerOfExpression = UnaryAddOrSubtractExpression, { [SP], '^', [SP], UnaryAddOrSubtractExpression } ;
    UnaryAddOrSubtractExpression = { ('+' | '-'), [SP] }, StringListNullOperatorExpression ;
    StringListNullOperatorExpression = PropertyOrLabelsExpression, { StringOperatorExpression | ListOperatorExpression | NullOperatorExpression } ;
    ListOperatorExpression = (SP, (I,N), [SP], PropertyOrLabelsExpression)
                           | ([SP], '[', Expression, ']')
                           | ([SP], '[', [Expression], '..', [Expression], ']')
                           ;
    StringOperatorExpression = ((SP, (S,T,A,R,T,S), SP, (W,I,T,H)) | (SP, (E,N,D,S), SP, (W,I,T,H)) | (SP, (C,O,N,T,A,I,N,S))), [SP], PropertyOrLabelsExpression ;
    NullOperatorExpression = (SP, (I,S), SP, (N,U,L,L))
                           | (SP, (I,S), SP, (N,O,T), SP, (N,U,L,L))
                           ;
    PropertyOrLabelsExpression = Atom, { [SP], PropertyLookup }, [[SP], NodeLabels] ;

    """
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
