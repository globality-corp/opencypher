from typing import Generic, List, TypeVar


T = TypeVar("T")


class NonEmptyList(Generic[T], List[T]):
    """
    Generic list type that enforces non-emptiness.

    """
    def __init__(self, arg: T, *args: T):
        super().__init__((arg,) + args)
