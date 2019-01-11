from opencypher.ast import (
    Cypher,
    RegularQuery,
    Union,
)


class CypherUnionBuilder(Cypher):
    """
    Extension of Cypher AST that supports unions.

    """
    def union(self, cypher: Cypher, all: bool = False) -> "CypherUnionBuilder":
        return CypherUnionBuilder(
            statement=RegularQuery(
                query=self.statement.query,
                items=(
                    *self.statement.items,
                    Union(
                        query=cypher.statement.query,
                        all=all,
                    ),
                    *cypher.statement.items,
                ),
            ),
        )

    def union_all(self, cypher: Cypher) -> "CypherUnionBuilder":
        return self.union(cypher, all=True)
