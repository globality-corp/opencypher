from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from opencypher.ast import (
    Cypher,
    NonEmptySequence,
    Order,
    Parameter,
    PatternElement,
    ReadingClause,
    ReturnItem,
    SinglePartReadQuery,
    SinglePartWriteQuery,
    UpdatingClause,
)
from opencypher.ast.expression import Parameterized
from opencypher.builder.clause import ClauseFactory
from opencypher.builder.return_ import ReturnFactory


class CypherWriteBuilder(Parameterized):

    def __init__(self,
                 updating_clause: UpdatingClause,
                 reading_clauses: Optional[List[ReadingClause]] = None,
                 clause_factory: Optional[ClauseFactory] = None,
                 return_factory: Optional[ReturnFactory] = None):
        self.updating_clauses: List[UpdatingClause] = [
            updating_clause,
        ]
        self.reading_clauses: List[ReadingClause] = reading_clauses or []
        self.clause_factory: ClauseFactory = clause_factory or ClauseFactory()
        self.return_factory: ReturnFactory = return_factory or ReturnFactory()

    def create(self, pattern_element: PatternElement) -> "CypherWriteBuilder":
        self.updating_clauses.append(
            self.clause_factory.create(pattern_element),
        )
        return self

    def delete(self, expression: str, *expressions: str, detach: bool = False) -> "CypherWriteBuilder":
        self.updating_clauses.append(
            self.clause_factory.delete(expression, *expressions, detach=detach),
        )
        return self

    def match(self, pattern_element: PatternElement) -> "CypherWriteBuilder":
        self.reading_clauses.append(
            self.clause_factory.match(pattern_element),
        )
        return self

    def merge(self, pattern_element: PatternElement) -> "CypherWriteBuilder":
        self.updating_clauses.append(
            self.clause_factory.merge(pattern_element),
        )
        return self

    def set(self, parameter: Parameter, *parameters: Parameter) -> "CypherWriteBuilder":
        self.updating_clauses.append(
            self.clause_factory.set(parameter, *parameters),
        )
        return self

    def ret(self,
            *items: ReturnItem,
            order: Optional[Order] = None,
            skip: Optional[int] = None,
            limit: Optional[int] = None) -> Cypher:
        return Cypher(
            statement=SinglePartWriteQuery(
                reading_clauses=self.reading_clauses,
                updating_clauses=NonEmptySequence[UpdatingClause](
                    self.updating_clauses[0],
                    *self.updating_clauses[1:],
                ),
                return_=self.return_factory.ret(
                    items[0],
                    *items[1:],
                    order=order,
                    skip=skip,
                    limit=limit,
                ) if items else None,
            ),
        )

    def __str__(self) -> str:
        return str(self.ret())

    def iter_parameters(self) -> Iterable[Parameter]:
        yield from self.ret().iter_parameters()


class CypherReadBuilder:
    def __init__(self,
                 reading_clause: Optional[ReadingClause] = None,
                 clause_factory: Optional[ClauseFactory] = None,
                 return_factory: Optional[ReturnFactory] = None):
        self.reading_clauses: List[ReadingClause] = [
            reading_clause,
        ] if reading_clause is not None else []
        self.clause_factory: ClauseFactory = clause_factory or ClauseFactory()
        self.return_factory: ReturnFactory = return_factory or ReturnFactory()

    def create(self, pattern_element: PatternElement) -> CypherWriteBuilder:
        return CypherWriteBuilder(
            self.clause_factory.create(pattern_element),
            reading_clauses=self.reading_clauses,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def delete(self, expression: str, *expressions: str, detach: bool = False) -> CypherWriteBuilder:
        return CypherWriteBuilder(
            self.clause_factory.delete(expression, *expressions, detach=detach),
            reading_clauses=self.reading_clauses,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def match(self, pattern_element: PatternElement) -> "CypherReadBuilder":
        self.reading_clauses.append(
            self.clause_factory.match(pattern_element),
        )
        return self

    def merge(self, pattern_element: PatternElement) -> CypherWriteBuilder:
        return CypherWriteBuilder(
            self.clause_factory.merge(pattern_element),
            reading_clauses=self.reading_clauses,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def set(self, parameter: Parameter, *parameters: Parameter) -> CypherWriteBuilder:
        return CypherWriteBuilder(
            self.clause_factory.set(parameter, *parameters),
            reading_clauses=self.reading_clauses,
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def ret(self,
            item: ReturnItem,
            *items: ReturnItem,
            order: Optional[Order] = None,
            skip: Optional[int] = None,
            limit: Optional[int] = None) -> Cypher:
        return Cypher(
            statement=SinglePartReadQuery(
                reading_clauses=self.reading_clauses,
                return_=self.return_factory.ret(
                    item,
                    *items,
                    order=order,
                    skip=skip,
                    limit=limit,
                ),
            ),
        )


@dataclass(frozen=True)
class CypherBuilder:
    clause_factory: ClauseFactory = field(default_factory=ClauseFactory)
    return_factory: ReturnFactory = field(default_factory=ReturnFactory)

    def create(self, pattern_element: PatternElement) -> CypherWriteBuilder:
        return CypherWriteBuilder(
            self.clause_factory.create(pattern_element),
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def delete(self, expression: str, *expressions: str, detach: bool = False) -> CypherWriteBuilder:
        return CypherWriteBuilder(
            self.clause_factory.delete(expression, *expressions, detach=detach),
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def match(self, pattern_element: PatternElement) -> CypherReadBuilder:
        return CypherReadBuilder(
            self.clause_factory.match(pattern_element),
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def merge(self, pattern_element: PatternElement) -> CypherWriteBuilder:
        return CypherWriteBuilder(
            self.clause_factory.merge(pattern_element),
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def set(self, parameter: Parameter, *parameters: Parameter) -> CypherWriteBuilder:
        return CypherWriteBuilder(
            self.clause_factory.set(parameter, *parameters),
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        )

    def ret(self,
            item: ReturnItem,
            *items: ReturnItem,
            order: Optional[Order] = None,
            skip: Optional[int] = None,
            limit: Optional[int] = None) -> Cypher:
        return CypherReadBuilder(
            clause_factory=self.clause_factory,
            return_factory=self.return_factory,
        ).ret(
            item,
            *items,
            order=order,
            skip=skip,
            limit=limit,
        )
