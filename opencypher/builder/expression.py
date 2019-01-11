from typing import Iterable, Optional, Sequence

from opencypher.ast import (
    Expression,
    ExpressionAlias,
    FunctionInvocation,
    FunctionName,
    MapLiteral,
    NonEmptySequence,
    Parameter,
    Variable,
)


class ExpressionBuilder(Expression):

    def as_(self, variable: Variable) -> ExpressionAlias:
        return ExpressionAlias(
            expression=self,
            variable=variable,
        )


expr = ExpressionBuilder


class Functions(FunctionInvocation):

    @classmethod
    def func(cls,
             name: FunctionName,
             expression: Expression,
             *expressions: Expression) -> ExpressionBuilder:
        return ExpressionBuilder(
            cls(
                name=name,
                expressions=NonEmptySequence[Expression](
                    expression,
                    *expressions,
                ),
            ),
        )

    @classmethod
    def count(cls,
              expression: Expression,
              *expressions: Expression) -> ExpressionBuilder:
        return cls.func(
            "count",
            expression,
            *expressions,
        )


func = Functions


def parameters(key_prefix: Optional[str] = None,
               name_prefix: Optional[str] = None,
               **kwargs: str) -> Sequence[Parameter]:
    return [
        Parameter(
            key=f"{key_prefix}.{key}" if key_prefix else key,
            name=f"{name_prefix}_{key}" if name_prefix else key,
            value=value,
        )
        for key, value in kwargs.items()
    ]


def properties(parameters: Iterable[Parameter] = ()) -> Optional[MapLiteral]:
    items = [
        (parameter.key, expr(parameter))
        for parameter in parameters
    ]

    if not items:
        return None

    return MapLiteral(items)


var = Variable
