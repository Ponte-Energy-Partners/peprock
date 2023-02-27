from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import collections.abc

    import peprock.typing


class EmptyIterableError(LookupError):
    def __init__(self: EmptyIterableError) -> None:
        super().__init__("Unable to determine min and max of empty iterable")


def min_and_max(
    __iterable: collections.abc.Iterable[peprock.typing.SupportsLessThanT],
    /,
) -> tuple[peprock.typing.SupportsLessThanT, peprock.typing.SupportsLessThanT]:
    min_: peprock.typing.SupportsLessThanT | None = None
    max_: peprock.typing.SupportsLessThanT | None = None
    for value in __iterable:
        if min_ is None:
            min_ = max_ = value
        elif value < min_:
            min_ = value
        elif max_ < value:  # type: ignore[operator]
            max_ = value

    if min_ is None or max_ is None:
        raise EmptyIterableError

    return min_, max_


__all__ = [
    "EmptyIterableError",
    "min_and_max",
]
