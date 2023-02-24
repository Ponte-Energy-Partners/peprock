# ruff: noqa: TCH003

import datetime
import functools


# noinspection PyTypeChecker
@functools.singledispatch
def is_naive(arg: datetime.date | datetime.time | datetime.datetime, /) -> bool:
    # See https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive

    msg: str = (
        f"expected datetime.date | datetime.time | datetime.datetime, got {arg!r}"
    )
    raise TypeError(msg)


@is_naive.register
def _(_: datetime.date, /) -> bool:
    return True


@is_naive.register
def _(d: datetime.datetime, /) -> bool:
    return d.tzinfo is None or d.tzinfo.utcoffset(d) is None


@is_naive.register
def _(t: datetime.time, /) -> bool:
    return t.tzinfo is None or t.tzinfo.utcoffset(None) is None


def is_aware(arg: datetime.date | datetime.time | datetime.datetime, /) -> bool:
    return not is_naive(arg)


__all__ = [
    "is_naive",
    "is_aware",
]
