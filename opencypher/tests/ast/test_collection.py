from hamcrest import assert_that, calling, has_length, raises

from opencypher.ast import NonEmptyList


def test_no_items():
    assert_that(
        calling(NonEmptyList[str]).with_args(),
        raises(TypeError),
    )


def test_one_item():
    assert_that(
        NonEmptyList[str]("foo"),
        has_length(1),
    )


def test_two_items():
    assert_that(
        NonEmptyList[str]("foo", "bar"),
        has_length(2),
    )


def test_varargs():
    assert_that(
        NonEmptyList[str](*["foo", "bar"]),
        has_length(2),
    )
