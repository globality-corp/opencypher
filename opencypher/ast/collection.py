from typing import Generic, overload, Sequence, TypeVar


T = TypeVar("T")


class NonEmptySequence(Generic[T], Sequence[T]):
    """
    Generic list type that enforces non-emptiness.

    """
    def __init__(self, arg: T, *args: T):
        self.items = (arg, *args)

    def __len__(self) -> int:
        return len(self.items)

    @overload
    def __getitem__(self, idx: int) -> T: ...

    @overload  # noqa: F811
    def __getitem__(self, s: slice) -> Sequence[T]: ...

    def __getitem__(self, idx):  # noqa: F811
        if isinstance(idx, slice):
            raise TypeError
        return self.items[idx]
