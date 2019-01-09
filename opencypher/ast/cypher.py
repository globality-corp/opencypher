from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Union

from opencypher.ast.create import Create
from opencypher.ast.delete import Delete
from opencypher.ast.expression import Parameter, Parameterized
from opencypher.ast.match import Match
from opencypher.ast.merge import Merge
from opencypher.ast.nonemptylist import stringify, NonEmptyList
from opencypher.ast.return_ import Return
from opencypher.ast.set import Set


ReadingClause = Union[
    Match,
    # omitted: Unwind
    # omitted: InQueryCall
]

UpdatingClause = Union[
    Create,
    Merge,
    Delete,
    Set,
    # omitted: Remove,
]


@dataclass(frozen=True)
class SinglePartReadQuery(Parameterized):
    return_: Return
    reading_clauses: List[ReadingClause] = field(default_factory=list)

    def __str__(self) -> str:
        if self.reading_clauses:
            return f"{stringify(self.reading_clauses)} {str(self.return_)}"
        else:
            return f"{str(self.return_)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for reading_clause in self.reading_clauses:
            yield from reading_clause.iter_parameters()


@dataclass(frozen=True)
class SinglePartWriteQuery(Parameterized):
    updating_clauses: NonEmptyList[UpdatingClause]
    reading_clauses: List[ReadingClause] = field(default_factory=list)
    return_: Optional[Return] = None

    def __str__(self) -> str:
        if self.reading_clauses:
            if self.return_:
                return f"{stringify(self.reading_clauses)} {stringify(self.updating_clauses)} {str(self.return_)}"
            else:
                return f"{stringify(self.reading_clauses)} {stringify(self.updating_clauses)}"
        else:
            if self.return_:
                return f"{stringify(self.updating_clauses)} {str(self.return_)}"
            else:
                return f"{stringify(self.updating_clauses)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for updating_clause in self.updating_clauses:
            yield from updating_clause.iter_parameters()
        for reading_clause in self.reading_clauses:
            yield from reading_clause.iter_parameters()


SinglePartQuery = Union[
    SinglePartReadQuery,
    SinglePartWriteQuery,
]


SingleQuery = Union[
    SinglePartQuery,
    # omitted: MultiPartQuery
]

RegularQuery = Union[
    SingleQuery,
    # omitted: List[Union]
]

Query = Union[
    RegularQuery,
    # omitted: StandaloneCall
]

Statement = Query


@dataclass(frozen=True)
class Cypher(Parameterized):
    statement: Statement

    def __str__(self):
        return str(self.statement)

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.statement.iter_parameters()
