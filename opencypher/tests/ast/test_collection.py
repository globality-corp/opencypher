from hamcrest import assert_that, calling, has_length, raises

from opencypher.ast.collection import NonEmptySequence


def test_no_items():
    assert_that(
        calling(NonEmptySequence[str]).with_args(),
        raises(TypeError),
    )


def test_one_item():
    assert_that(
        NonEmptySequence[str]("foo"),
        has_length(1),
    )


def test_two_items():
    assert_that(
        NonEmptySequence[str]("foo", "bar"),
        has_length(2),
    )


def test_varargs():
    assert_that(
        NonEmptySequence[str](*["foo", "bar"]),
        has_length(2),
    )
