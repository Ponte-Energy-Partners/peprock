import datetime

import pytest

import peprock.datetime


@pytest.mark.parametrize(
    ("constant", "expected"),
    [
        (peprock.datetime.ONE_MICROSECOND, datetime.timedelta(microseconds=1)),
        (peprock.datetime.ONE_MILLISECOND, datetime.timedelta(milliseconds=1)),
        (peprock.datetime.ONE_SECOND, datetime.timedelta(seconds=1)),
        (peprock.datetime.ONE_MINUTE, datetime.timedelta(minutes=1)),
        (peprock.datetime.ONE_HOUR, datetime.timedelta(hours=1)),
        (peprock.datetime.ONE_DAY, datetime.timedelta(days=1)),
        (peprock.datetime.ONE_WEEK, datetime.timedelta(weeks=1)),
    ],
)
def test_constants(constant, expected):
    assert constant == expected
