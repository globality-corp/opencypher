# opencypher

[OpenCypher](https://www.opencypher.org/) AST and Builder API

OpenCypher defines an _abstract syntax tree_ based on the published OpenCypher
[EBNF grammar](https://s3.amazonaws.com/artifacts.opencypher.org/cypher.ebnf)
and a builder-oriented API for constructing Cypher queries.

OpenCypher leans heavily on Python 3.7 `dataclasses` and `typing`.


## Setup

    pip install opencypher


## Usage

The core API exposes a fluent builder interface for constructing queries and patterns:

    from opencypher.api import match, node

    query = match(
        node("person", "Person").rel_in().node("pet", "Pet")
    ).ret(
        "person",
        "pet",
    )

    print(query)  #  MATCH (person:Person)-[]->(pet :Pet) RETURN person, pet

The builder supports chaining patterns and chaining clauses; queries may terminate on either
a return statement (`.ret()`) or on any updating clause (e.g. `create()`, `delete()`, `merge()`,
and so forth.

    from opencypher.api import match, node

    query = match(
        node("alice", "Person", {"name": "Alice"}),
    ).match(
        node("bob", "Person", {"name": "Bob"}),
    ).merge(
        node("bob").rel_in(types="IS_FRIENDS_WITH").node("alice"),
    ).merge(
        node("alice").rel_in(types="IS_FRIENDS_WITH").node("bob"),
    )

The resulting `Cypher` query object integrates with -- but does not depend on -- the
[Neo4J Python driver](https://github.com/neo4j/neo4j-python-driver):

    from neo4j import GraphDatabase

    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    with driver.session() as session:
        session.run(str(query), dict(query))


## Caveats

Some compromises have been made with respect to the completeness of the AST:

 1. The grammar for expressions (and literals, atoms, etc.) has been deliberately simplified
    and reduces to `str` in many cases. The expression grammar is likely to get more complete
    over time.

 2. Some forms of argumementation (e.g. `Set` items) are not easy to construct using the builder
    API (although these remain available within the AST).

 3. Several top level query clauses are not yet implemented, including:

     -  `CALL`
     -  `WITH`

 4. Parameters do not automatically generate unique identifiers/prefixes. Parameter names will be
    derived from variable names where known, but no fallback exists yet for anonyomous pattern terms.

 5. Parameters do not support numeric values (`$1`); symbolic names (`$foo`) *are* supported.
