from opencypher.builder.expression import func, expr, parameters, properties, var
from opencypher.builder.cypher import CypherBuilder
from opencypher.builder.pattern import node
from opencypher.builder.return_ import asc, desc, order


# default builder
cypher = CypherBuilder

# shortcuts usin default builder
create = cypher().create
delete = cypher().delete
match = cypher().match
merge = cypher().merge
remove = cypher().remove
ret = cypher().ret
set = cypher().set
unwind = cypher().unwind


__all__ = [
    "asc",
    "desc",
    "create",
    "cypher",
    "delete",
    "expr",
    "func",
    "match",
    "merge",
    "node",
    "order",
    "parameters",
    "properties",
    "remove",
    "ret",
    "set",
    "unwind",
    "var",
]
