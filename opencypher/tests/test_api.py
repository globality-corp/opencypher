from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

from opencypher.api import (
    asc,
    match,
    node,
    parameters,
    properties,
)


def test_api():
    ast = match(
        node(
            "foo",
            "FOO",
            properties=properties(
                parameters(
                    name_prefix="foo",
                    bar="baz",
                ),
            ),
        ).rel_in(
            None,
            "Bar",
        ).node(
            "baz",
            "BAZ",
            properties=properties(
                parameters(
                    name_prefix="baz",
                    bar="foo",
                ),
            ),
        ),
    ).delete(
        "foo",
        "baz",
    ).ret(
        "foo",
        "baz",
        order=asc("foo", "bar"),
    )

    assert_that(
        str(ast),
        is_(equal_to(
            "MATCH (foo:FOO {bar: $foo_bar})<-[:Bar]-(baz:BAZ {bar: $baz_bar}) "
            "DELETE foo, baz "
            "RETURN foo, baz ORDER BY foo ASCENDING, bar ASCENDING",
        )),
    )
    assert_that(
        dict(ast),
        is_(equal_to(dict(
            foo_bar="baz",
            baz_bar="foo",
        ))),
    )


def test_readme_query():
    query = match(
        node("person", "Person").rel_in().node("pet", "Pet")
    ).ret(
        "person",
        "pet",
    )
    assert_that(
        str(query),
        is_(equal_to(
            "MATCH (person:Person)<-[]-(pet:Pet) RETURN person, pet",
        )),
    )


def test_readme_update():
    query = match(
        node("alice", "Person", {"name": "Alice"}),
    ).match(
        node("bob", "Person", {"name": "Bob"}),
    ).merge(
        node("bob").rel_in(types="IS_FRIENDS_WITH").node("alice"),
    ).merge(
        node("alice").rel_in(types="IS_FRIENDS_WITH").node("bob"),
    )

    assert_that(
        str(query),
        is_(equal_to(
            "MATCH (alice:Person {name: $alice_name}) "
            "MATCH (bob:Person {name: $bob_name}) "
            "MERGE (bob)<-[:IS_FRIENDS_WITH]-(alice) "
            "MERGE (alice)<-[:IS_FRIENDS_WITH]-(bob)"
        )),
    )
    assert_that(
        dict(query),
        is_(equal_to(dict(
            alice_name="Alice",
            bob_name="Bob",
        ))),
    )
