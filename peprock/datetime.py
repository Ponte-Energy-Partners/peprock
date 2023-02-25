# ruff: noqa: TCH003

import datetime
import functools
import typing

# constants
ONE_MICROSECOND: typing.Final[datetime.timedelta] = datetime.timedelta(microseconds=1)
ONE_MILLISECOND: typing.Final[datetime.timedelta] = datetime.timedelta(milliseconds=1)
ONE_SECOND: typing.Final[datetime.timedelta] = datetime.timedelta(seconds=1)
ONE_MINUTE: typing.Final[datetime.timedelta] = datetime.timedelta(minutes=1)
ONE_HOUR: typing.Final[datetime.timedelta] = datetime.timedelta(hours=1)
ONE_DAY: typing.Final[datetime.timedelta] = datetime.timedelta(days=1)
ONE_WEEK: typing.Final[datetime.timedelta] = datetime.timedelta(weeks=1)


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


class EnsureAwareError(ValueError):
    def __init__(
        self,
        arg: datetime.datetime,
        /,
        *,
        assumed_tz: datetime.tzinfo | None = None,
        target_tz: datetime.tzinfo | None = None,
    ) -> None:
        super().__init__(
            f"Unable to ensure awareness of '{arg!r}' using "
            f"'{assumed_tz=}' and '{target_tz=}'",
        )


def ensure_aware(
    arg: datetime.datetime,
    /,
    *,
    assumed_tz: datetime.tzinfo | None = None,
    target_tz: datetime.tzinfo | None = None,
) -> datetime.datetime:
    if arg.tzinfo is None:
        if assumed_tz is None:
            raise EnsureAwareError(
                arg,
                assumed_tz=assumed_tz,
                target_tz=target_tz,
            )

        arg = arg.replace(tzinfo=assumed_tz)

    if target_tz:
        return arg.astimezone(tz=target_tz)

    return arg


__all__ = [
    "ONE_MICROSECOND",
    "ONE_MILLISECOND",
    "ONE_SECOND",
    "ONE_MINUTE",
    "ONE_HOUR",
    "ONE_DAY",
    "ONE_WEEK",
    "is_naive",
    "is_aware",
    "EnsureAwareError",
    "ensure_aware",
]
