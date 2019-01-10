from dataclasses import dataclass, field
from typing import Optional, Sequence

from opencypher.ast import (
    NonEmptySequence,
    Order,
    Parameter,
    PatternElement,
    ReadingClause,
    RegularQuery,
    ReturnItem,
    SinglePartReadQuery,
    UpdatingClause,
)
from opencypher.builder.clause import ClauseFactory
from opencypher.builder.return_ import ReturnFactory
from opencypher.builder.union import CypherUnionBuilder
from opencypher.builder.write import CypherWriteBuilder


@dataclass(frozen=True)
class CypherBuilder:
    """
    Builder for Cypher AST instances *using* single part read queries.

    The transitions are:

        ( :create :delete :merge :set ) --> ( :CypherWriteBuilder )
        ( :match )                      --> ( :CypherBuilder )
        ( :ret )                        --> ( :CypherUnionBuilder )

    """
    reading_clauses: Sequence[ReadingClause] = ()
    clause_factory: ClauseFactory = field(default_factory=ClauseFactory)
    return_factory: ReturnFactory = field(default_factory=ReturnFactory)

    def create(self, pattern_element: PatternElement) -> CypherWriteBuilder:
        return CypherWriteBuilder.make(
            NonEmptySequence[UpdatingClause](
                self.clause_factory.create(pattern_element),
            ),
            reading_clauses=self.reading_clauses,
            return_=None,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def delete(self, expression: str, *expressions: str, detach: bool = False) -> CypherWriteBuilder:
        return CypherWriteBuilder.make(
            NonEmptySequence[UpdatingClause](
                self.clause_factory.delete(expression, *expressions, detach=detach),
            ),
            reading_clauses=self.reading_clauses,
            return_=None,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def match(self, pattern_element: PatternElement) -> "CypherBuilder":
        reading_clause = self.clause_factory.match(pattern_element)

        return CypherBuilder(
            reading_clauses=(*self.reading_clauses, reading_clause),
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def merge(self, pattern_element: PatternElement) -> CypherWriteBuilder:
        return CypherWriteBuilder.make(
            NonEmptySequence[UpdatingClause](
                self.clause_factory.merge(pattern_element),
            ),
            reading_clauses=self.reading_clauses,
            return_=None,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def set(self, parameter: Parameter, *parameters: Parameter) -> CypherWriteBuilder:
        return CypherWriteBuilder.make(
            NonEmptySequence[UpdatingClause](
                self.clause_factory.set(parameter, *parameters),
            ),
            reading_clauses=self.reading_clauses,
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
        return CypherUnionBuilder(
            statement=RegularQuery(
                query=SinglePartReadQuery(
                    reading_clauses=self.reading_clauses,
                    return_=self.return_factory.ret(
                        item,
                        *items,
                        order=order,
                        skip=skip,
                        limit=limit,
                    ),
                ),
            ),
        )
