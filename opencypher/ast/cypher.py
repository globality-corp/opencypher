from dataclasses import dataclass
from typing import Iterable

from opencypher.ast.parameter import Parameter, Parameterized
from opencypher.ast.query import Query


"""
Statement = Query ;

"""
Statement = Query


@dataclass(frozen=True)
class Cypher(Parameterized):
    """
    Cypher = [SP], Statement, [[SP], ';'], [SP], EOI ;

    """
    statement: Statement

    def __str__(self):
        return str(self.statement)

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.statement.iter_parameters()
