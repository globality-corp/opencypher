from typing import Iterable


def str_join(items: Iterable, sep: str = " ") -> str:
    return sep.join(str(item) for item in items)
