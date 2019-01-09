from dataclasses import dataclass
from typing import Iterable, Optional, Sequence, Union

from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.create import Create
from opencypher.ast.delete import Delete
from opencypher.ast.expression import Parameter, Parameterized
from opencypher.ast.formatting import str_join
from opencypher.ast.match import Match
from opencypher.ast.merge import Merge
from opencypher.ast.return_ import Return
from opencypher.ast.set import Set


"""
ReadingClause = Match
              | Unwind
              | InQueryCall
              ;

"""
ReadingClause = Union[
    Match,
    # omitted: Unwind
    # omitted: InQueryCall
]

"""
UpdatingClause = Create
               | Merge
               | Delete
               | Set
               | Remove
               ;

"""
UpdatingClause = Union[
    Create,
    Merge,
    Delete,
    Set,
    # omitted: Remove,
]


@dataclass(frozen=True)
class SinglePartReadQuery(Parameterized):
    """
    SinglePartQuery = ({ ReadingClause, [SP] }, Return)
                    | ...
                    ;
    """
    return_: Return
    reading_clauses: Optional[Sequence[ReadingClause]] = None

    def __str__(self) -> str:
        if self.reading_clauses:
            return f"{str_join(self.reading_clauses)} {str(self.return_)}"
        else:
            return f"{str(self.return_)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        if self.reading_clauses:
            for reading_clause in self.reading_clauses:
                yield from reading_clause.iter_parameters()


@dataclass(frozen=True)
class SinglePartWriteQuery(Parameterized):
    """
    SinglePartQuery = ...
                    | ({ ReadingClause, [SP] }, UpdatingClause, { [SP], UpdatingClause }, [[SP], Return])
                    ;

    """
    updating_clauses: NonEmptySequence[UpdatingClause]
    reading_clauses: Optional[Sequence[ReadingClause]] = None
    return_: Optional[Return] = None

    def __str__(self) -> str:
        if self.reading_clauses:
            if self.return_:
                return f"{str_join(self.reading_clauses)} {str_join(self.updating_clauses)} {str(self.return_)}"
            else:
                return f"{str_join(self.reading_clauses)} {str_join(self.updating_clauses)}"
        else:
            if self.return_:
                return f"{str_join(self.updating_clauses)} {str(self.return_)}"
            else:
                return f"{str_join(self.updating_clauses)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for updating_clause in self.updating_clauses:
            yield from updating_clause.iter_parameters()
        if self.reading_clauses:
            for reading_clause in self.reading_clauses:
                yield from reading_clause.iter_parameters()


"""
SinglePartQuery = ({ ReadingClause, [SP] }, Return)
                | ({ ReadingClause, [SP] }, UpdatingClause, { [SP], UpdatingClause }, [[SP], Return])
                ;

"""
SinglePartQuery = Union[
    SinglePartReadQuery,
    SinglePartWriteQuery,
]


"""
SingleQuery = SinglePartQuery
            | MultiPartQuery
            ;

"""
SingleQuery = Union[
    SinglePartQuery,
    # omitted: MultiPartQuery
]

"""
RegularQuery = SingleQuery, { [SP], Union } ;

"""
RegularQuery = Union[
    SingleQuery,
    # omitted: Union
]

"""
Query = RegularQuery
      | StandaloneCall
      ;

"""
Query = Union[
    RegularQuery,
    # omitted: StandaloneCall
]

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
