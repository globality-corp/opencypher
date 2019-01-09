from dataclasses import dataclass

from opencypher.ast.expression import Expression


@dataclass(frozen=True)
class Skip:
    expression: Expression

    def __str__(self) -> str:
        return f"SKIP {str(self.expression)}"


@dataclass(frozen=True)
class Limit:
    expression: Expression

    def __str__(self) -> str:
        return f"LIMIT {str(self.expression)}"
