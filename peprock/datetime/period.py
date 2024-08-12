"""Datetime period model.

Examples
--------
>>> period = Period(
...     start=datetime.datetime(2022, 1, 1, 12, 0),
...     end=datetime.datetime(2022, 1, 2, 12, 0),
... )
>>> period.duration
datetime.timedelta(days=1)
>>> period.midpoint
datetime.datetime(2022, 1, 2, 0, 0)
>>> datetime.datetime(2022, 1, 1) in period
False
>>> period.start in period
True
>>> period.midpoint in period
True
>>> period.end in period
True
>>> datetime.datetime(2022, 1, 3) in period
False
>>> period in period
True
>>> Period(
...     start=datetime.datetime(2022, 1, 1),
...     end=datetime.datetime(2022, 1, 3),
... ) in period
False


"""

import collections.abc
import dataclasses
import datetime
import functools
import sys

if sys.version_info >= (3, 11):
    from typing import Self  # pragma: no cover
else:
    from typing_extensions import Self  # pragma: no cover


@dataclasses.dataclass(frozen=True)
class Period(
    collections.abc.Container["Period | datetime.datetime"],
):
    """Datetime period supporting arithmetic operations."""

    start: datetime.datetime
    end: datetime.datetime

    @functools.cached_property
    def duration(self: Self) -> datetime.timedelta:
        """Return duration of period."""
        return self.end - self.start

    @functools.cached_property
    def midpoint(self: Self) -> datetime.datetime:
        """Return midpoint of period."""
        return self.start + self.duration / 2

    def __contains__(self: Self, item: object) -> bool:
        """Return True if item is in period."""
        match item:
            case Period():
                # noinspection PyUnresolvedReferences
                return self.start <= item.start and item.end <= self.end
            case datetime.datetime():
                # noinspection PyTypeChecker
                return self.start <= item <= self.end

        msg: str = f"expected peprock.datetime.Period | datetime.datetime, got {item!r}"
        raise TypeError(msg)


__all__ = [
    "Period",
]
