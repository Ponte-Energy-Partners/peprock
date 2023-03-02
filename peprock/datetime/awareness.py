"""Timezone awareness helpers.

See https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
for definitions.
"""

from __future__ import annotations

import datetime  # noqa: TCH003
import functools


# noinspection PyTypeChecker
@functools.singledispatch
def is_naive(arg: datetime.date | datetime.time | datetime.datetime, /) -> bool:
    """Determine if arg is timezone naive and return a bool."""
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
    """Determine if arg is timezone aware and return a bool."""
    return not is_naive(arg)


class EnsureAwareError(ValueError):
    """Unable to ensure awareness."""

    def __init__(
        self: EnsureAwareError,
        arg: datetime.datetime,
        /,
        *,
        assumed_tz: datetime.tzinfo | None = None,
        target_tz: datetime.tzinfo | None = None,
    ) -> None:
        """Initialize EnsureAwareError with arguments used in ensure_aware()."""
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
    """Ensure timezone awareness of arg."""
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
    "is_naive",
    "is_aware",
    "EnsureAwareError",
    "ensure_aware",
]
