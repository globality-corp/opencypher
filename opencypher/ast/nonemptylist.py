from typing import Generic, Iterable, List, TypeVar


def stringify(items: Iterable, sep: str = " ") -> str:
    return sep.join(str(item) for item in items)


T = TypeVar("T")


class NonEmptyList(Generic[T], List[T]):
    def __init__(self, arg: T, *args: T):
        super().__init__((arg,) + args)
