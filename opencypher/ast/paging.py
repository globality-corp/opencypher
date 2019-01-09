from dataclasses import dataclass

from opencypher.ast.expression import Expression


@dataclass(frozen=True)
class Skip:
    """
    Skip = (S,K,I,P), SP, Expression ;

    """
    expression: Expression

    def __str__(self) -> str:
        return f"SKIP {str(self.expression)}"


@dataclass(frozen=True)
class Limit:
    """
    Limit = (L,I,M,I,T), SP, Expression ;

    """
    expression: Expression

    def __str__(self) -> str:
        return f"LIMIT {str(self.expression)}"
