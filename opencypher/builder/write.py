from dataclasses import dataclass, field
from typing import cast, Optional, Sequence, Tuple

from opencypher.ast import (
    NonEmptySequence,
    Order,
    Parameter,
    PatternElement,
    ReadingClause,
    RegularQuery,
    Return,
    ReturnItem,
    SinglePartWriteQuery,
    UpdatingClause,
)
from opencypher.builder.clause import ClauseFactory
from opencypher.builder.return_ import ReturnFactory
from opencypher.builder.union import CypherUnionBuilder


@dataclass(frozen=True)
class CypherWriteBuilder(CypherUnionBuilder):
    """
    Builder for Cypher AST instances *using* single part write queries.

    The transitions are:

        ( :create :delete :match :merge :set ) --> ( :CypherWriteBuilder )
        ( :ret )                               --> ( :CypherUnionBuilder )

    """
    clause_factory: ClauseFactory = field(default_factory=ClauseFactory)
    return_factory: ReturnFactory = field(default_factory=ReturnFactory)

    def create(self, pattern_element: PatternElement) -> "CypherWriteBuilder":
        query = cast(SinglePartWriteQuery, self.statement.query)
        updating_clause = self.clause_factory.create(pattern_element)

        return self.make(
            updating_clauses=query.updating_clauses + (updating_clause, ),
            reading_clauses=query.reading_clauses,
            return_=None,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def delete(self, expression: str, *expressions: str, detach: bool = False) -> "CypherWriteBuilder":
        query = cast(SinglePartWriteQuery, self.statement.query)
        updating_clause = self.clause_factory.delete(expression, *expressions, detach=detach)

        return self.make(
            updating_clauses=query.updating_clauses + (updating_clause, ),
            reading_clauses=query.reading_clauses,
            return_=None,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def match(self, pattern_element: PatternElement) -> "CypherWriteBuilder":
        query = cast(SinglePartWriteQuery, self.statement.query)
        reading_clause = self.clause_factory.match(pattern_element)

        return self.make(
            updating_clauses=query.updating_clauses,
            reading_clauses=(*query.reading_clauses, reading_clause),
            return_=None,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def merge(self, pattern_element: PatternElement) -> "CypherWriteBuilder":
        query = cast(SinglePartWriteQuery, self.statement.query)
        updating_clause = self.clause_factory.merge(pattern_element)

        return self.make(
            updating_clauses=query.updating_clauses + (updating_clause, ),
            reading_clauses=query.reading_clauses,
            return_=None,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def remove(self, target: Tuple[str, str], *targets: Tuple[str, str]) -> "CypherWriteBuilder":
        query = cast(SinglePartWriteQuery, self.statement.query)
        updating_clause = self.clause_factory.remove(target, *targets)

        return CypherWriteBuilder.make(
            updating_clauses=query.updating_clauses + (updating_clause, ),
            reading_clauses=query.reading_clauses,
            return_=None,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def set(self, parameter: Parameter, *parameters: Parameter) -> "CypherWriteBuilder":
        query = cast(SinglePartWriteQuery, self.statement.query)
        updating_clause = self.clause_factory.set(parameter, *parameters)

        return self.make(
            updating_clauses=query.updating_clauses + (updating_clause, ),
            reading_clauses=query.reading_clauses,
            return_=None,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def ret(self,
            item: ReturnItem,
            *items: ReturnItem,
            order: Optional[Order] = None,
            skip: Optional[int] = None,
            limit: Optional[int] = None) -> CypherUnionBuilder:
        query = cast(SinglePartWriteQuery, self.statement.query)
        return_ = self.return_factory.ret(
            item,
            *items,
            order=order,
            skip=skip,
            limit=limit,
        )

        return self.make(
            updating_clauses=query.updating_clauses,
            reading_clauses=query.reading_clauses,
            return_=return_,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    @classmethod
    def make(cls,
             updating_clauses: NonEmptySequence[UpdatingClause],
             reading_clauses: Sequence[ReadingClause],
             return_: Optional[Return],
             clause_factory: ClauseFactory,
             return_factory: ReturnFactory) -> "CypherWriteBuilder":

        return cls(
            statement=RegularQuery(
                query=SinglePartWriteQuery(
                    updating_clauses=updating_clauses,
                    reading_clauses=reading_clauses,
                    return_=return_,
                ),
            ),
            clause_factory=clause_factory,
            return_factory=return_factory,
        )
