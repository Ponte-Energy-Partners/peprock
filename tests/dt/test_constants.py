import datetime

import pytest

import peprock.dt


@pytest.mark.parametrize(
    ("constant", "expected"),
    [
        (peprock.dt.ONE_MICROSECOND, datetime.timedelta(microseconds=1)),
        (peprock.dt.ONE_MILLISECOND, datetime.timedelta(milliseconds=1)),
        (peprock.dt.ONE_SECOND, datetime.timedelta(seconds=1)),
        (peprock.dt.ONE_MINUTE, datetime.timedelta(minutes=1)),
        (peprock.dt.ONE_HOUR, datetime.timedelta(hours=1)),
        (peprock.dt.ONE_DAY, datetime.timedelta(days=1)),
        (peprock.dt.ONE_WEEK, datetime.timedelta(weeks=1)),
    ],
)
def test_constants(constant, expected):
    assert constant == expected
