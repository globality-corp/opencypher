# opencypher

[OpenCypher](https://www.opencypher.org/) AST and Builder API

OpenCypher defines an _abstract syntax tree_ based on the published OpenCypher
[EBNF grammar](https://s3.amazonaws.com/artifacts.opencypher.org/cypher.ebnf)
and a builder-oriented API for constructing Cypher queries.

OpenCypher leans heavily on Python 3.7 `dataclasses` and `typing`.


## Usage

The core API exposes a fluent builder interface for constructing queries and patterns:

    from opencypher.api import match, node

    query = match(
        node("person", "Person").rel_in().node("pet", "Pet")
    ).ret(
        "person",
        "pet",
    )

    print(query)  #  MATCH ( person:Person ) - [ ] -> ( pet:Pet ) RETURN person, pet

The resulting `Cypher` query object integrates with -- but does not depend on -- the
[Neo4J Python driver](https://github.com/neo4j/neo4j-python-driver):

    from neo4j import GraphDatabase

    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

    with driver.session() as session:
        session.run(str(query), dict(query))
