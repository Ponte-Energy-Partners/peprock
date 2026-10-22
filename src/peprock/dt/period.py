"""Datetime period model.

Examples
--------
>>> period = Period(
...     start=dt.datetime(2022, 1, 1, 12, 0),
...     end=dt.datetime(2022, 1, 2, 12, 0),
... )
>>> period.duration
datetime.timedelta(days=1)
>>> period.midpoint
datetime.datetime(2022, 1, 2, 0, 0)
>>> dt.datetime(2022, 1, 1) in period
False
>>> period.start in period
True
>>> period.midpoint in period
True
>>> period.end in period
True
>>> dt.datetime(2022, 1, 3) in period
False
>>> period in period
True
>>> Period(
...     start=dt.datetime(2022, 1, 1),
...     end=dt.datetime(2022, 1, 3),
... ) in period
False


"""

import collections.abc
import dataclasses
import datetime as dt
import functools
import typing


@dataclasses.dataclass(frozen=True)
class Period(
    collections.abc.Container["Period | dt.datetime"],
):
    """Datetime period supporting arithmetic operations."""

    start: dt.datetime
    end: dt.datetime

    @functools.cached_property
    def duration(self: typing.Self) -> dt.timedelta:
        """Return duration of period."""
        return self.end - self.start

    @functools.cached_property
    def midpoint(self: typing.Self) -> dt.datetime:
        """Return midpoint of period."""
        return self.start + self.duration / 2

    def __contains__(self: typing.Self, item: object) -> bool:
        """Return True if item is in period."""
        match item:
            case Period():
                return self.start <= item.start and item.end <= self.end
            case dt.datetime():
                return self.start <= item <= self.end

        msg: str = f"expected peprock.dt.Period | datetime.datetime, got {item!r}"
        raise TypeError(msg)


__all__ = [
    "Period",
]
