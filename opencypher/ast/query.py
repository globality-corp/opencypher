from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence, Union as Choice

from opencypher.ast.clause import ReadingClause, UpdatingClause
from opencypher.ast.collection import NonEmptySequence
from opencypher.ast.formatting import str_join
from opencypher.ast.parameter import Parameter, Parameterized
from opencypher.ast.return_ import Return
from opencypher.ast.with_ import With


@dataclass(frozen=True)
class SinglePartReadQuery(Parameterized):
    """
    SinglePartQuery = ({ ReadingClause, [SP] }, Return)
                    | ...
                    ;
    """
    return_: Return
    reading_clauses: Sequence[ReadingClause] = ()

    def __str__(self) -> str:
        if self.reading_clauses:
            return f"{str_join(self.reading_clauses)} {str(self.return_)}"
        else:
            return f"{str(self.return_)}"

    def iter_parameters(self) -> Iterable[Parameter]:
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
    reading_clauses: Sequence[ReadingClause] = ()
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


@dataclass(frozen=True)
class WithSubQuery(Parameterized):
    """
    MultiPartQuery = { { ReadingClause, [SP] }, { UpdatingClause, [SP] }, With, [SP] }

    """
    with_: With
    updating_clauses: Sequence[UpdatingClause] = field(default_factory=list)
    reading_clauses: Sequence[ReadingClause] = field(default_factory=list)

    def __str__(self) -> str:
        if self.reading_clauses:
            if self.updating_clauses:
                return f"{str_join(self.reading_clauses)} {str_join(self.updating_clauses)} {str(self.with_)}"  # noqa:E501
            else:
                return f"{str_join(self.reading_clauses)} {str(self.with_)}"
        else:
            if self.updating_clauses:
                return f"{str_join(self.updating_clauses)} {str(self.with_)}"
            else:
                return f"{str(self.with_)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for reading_clause in self.reading_clauses:
            yield from reading_clause.iter_parameters()
        for updating_clause in self.updating_clauses:
            yield from updating_clause.iter_parameters()
        yield from self.with_.iter_parameters()


@dataclass(frozen=True)
class MultiPartQuery(Parameterized):
    """
    MultiPartQuery = { { ReadingClause, [SP] }, { UpdatingClause, [SP] }, With, [SP] }-, SinglePartQuery ;

    """
    single_part_query: "SinglePartQuery"
    with_sub_querys: NonEmptySequence[WithSubQuery]

    def __str__(self) -> str:
        return f"{str(self.with_sub_querys)} {str(self.single_part_query)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        for with_sub_query in self.with_sub_querys:
            yield from with_sub_query.iter_parameters()
        yield from self.single_part_query.iter_parameters()


"""
SinglePartQuery = ({ ReadingClause, [SP] }, Return)
                | ({ ReadingClause, [SP] }, UpdatingClause, { [SP], UpdatingClause }, [[SP], Return])
                ;

"""
SinglePartQuery = Choice[
    SinglePartReadQuery,
    SinglePartWriteQuery,
]


"""
SingleQuery = SinglePartQuery
            | MultiPartQuery
            ;

"""
SingleQuery = Choice[
    SinglePartQuery,
    MultiPartQuery,
]


@dataclass(frozen=True)
class Union:
    query: SingleQuery
    all: bool = False

    def __str__(self) -> str:
        if self.all:
            return f"UNION ALL {str(self.query)}"
        else:
            return f"UNION {str(self.query)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.query.iter_parameters()


@dataclass(frozen=True)
class RegularQuery(Parameterized):
    """
    RegularQuery = SingleQuery, { [SP], Union } ;

    """
    query: SingleQuery
    items: Sequence[Union] = ()

    def __str__(self) -> str:
        if self.items:
            return f"{str(self.query)} {str_join(self.items)}"
        else:
            return f"{str(self.query)}"

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.query.iter_parameters()
        if self.items:
            for item in self.items:
                yield from item.iter_parameters()


"""
Query = RegularQuery
      | StandaloneCall
      ;

"""
Query = Choice[
    RegularQuery,
    # omitted: StandaloneCall
]
