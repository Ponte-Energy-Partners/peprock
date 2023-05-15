"""Timedelta constants.

Examples
--------
>>> dt = datetime.datetime(2023, 3, 2, 21, 17, 12)
>>> dt + ONE_HOUR + 5 * ONE_SECOND
datetime.datetime(2023, 3, 2, 22, 17, 17)

"""

import datetime
import typing

ONE_MICROSECOND: typing.Final[datetime.timedelta] = datetime.timedelta(microseconds=1)
ONE_MILLISECOND: typing.Final[datetime.timedelta] = datetime.timedelta(milliseconds=1)
ONE_SECOND: typing.Final[datetime.timedelta] = datetime.timedelta(seconds=1)
ONE_MINUTE: typing.Final[datetime.timedelta] = datetime.timedelta(minutes=1)
ONE_HOUR: typing.Final[datetime.timedelta] = datetime.timedelta(hours=1)
ONE_DAY: typing.Final[datetime.timedelta] = datetime.timedelta(days=1)
ONE_WEEK: typing.Final[datetime.timedelta] = datetime.timedelta(weeks=1)

__all__ = [
    "ONE_MICROSECOND",
    "ONE_MILLISECOND",
    "ONE_SECOND",
    "ONE_MINUTE",
    "ONE_HOUR",
    "ONE_DAY",
    "ONE_WEEK",
]
