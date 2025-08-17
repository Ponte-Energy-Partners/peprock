# ruff: noqa: DTZ001

import datetime
import typing
import zoneinfo

import pytest

import peprock.dt

_OFFSET: typing.Final[datetime.timedelta] = datetime.timedelta(hours=1)
_NAIVE_DATETIME_1: typing.Final[datetime.datetime] = datetime.datetime(
    2023,
    12,
    24,
    12,
    34,
    56,
)
_NAIVE_DATETIME_2: typing.Final[datetime.datetime] = _NAIVE_DATETIME_1 + _OFFSET
_AWARE_DATETIME_1: typing.Final[datetime.datetime] = _NAIVE_DATETIME_1.replace(
    tzinfo=datetime.timezone.utc,
)
_AWARE_DATETIME_2: typing.Final[datetime.datetime] = _AWARE_DATETIME_1 + _OFFSET
_VARIABLE_OFFSET_ZONE_INFO: typing.Final[zoneinfo.ZoneInfo] = zoneinfo.ZoneInfo(
    "Europe/Paris",
)


class TestGenericPeriod:
    @pytest.mark.parametrize(
        ("start", "end", "expected"),
        [
            (
                _NAIVE_DATETIME_1,
                _NAIVE_DATETIME_1,
                (datetime.timedelta(), _NAIVE_DATETIME_1),
            ),
            (
                _NAIVE_DATETIME_1,
                _NAIVE_DATETIME_2,
                (_OFFSET, _NAIVE_DATETIME_1 + _OFFSET / 2),
            ),
            (
                _NAIVE_DATETIME_1,
                _AWARE_DATETIME_1,
                TypeError,
            ),
            (
                _NAIVE_DATETIME_1,
                _AWARE_DATETIME_2,
                TypeError,
            ),
            (
                _NAIVE_DATETIME_2,
                _NAIVE_DATETIME_1,
                (-_OFFSET, _NAIVE_DATETIME_1 + _OFFSET / 2),
            ),
            (
                _NAIVE_DATETIME_2,
                _NAIVE_DATETIME_2,
                (datetime.timedelta(), _NAIVE_DATETIME_2),
            ),
            (
                _NAIVE_DATETIME_2,
                _AWARE_DATETIME_1,
                TypeError,
            ),
            (
                _NAIVE_DATETIME_2,
                _AWARE_DATETIME_2,
                TypeError,
            ),
            (
                _AWARE_DATETIME_1,
                _NAIVE_DATETIME_1,
                TypeError,
            ),
            (
                _AWARE_DATETIME_1,
                _NAIVE_DATETIME_2,
                TypeError,
            ),
            (
                _AWARE_DATETIME_1,
                _AWARE_DATETIME_1,
                (datetime.timedelta(), _AWARE_DATETIME_1),
            ),
            (
                _AWARE_DATETIME_1,
                _AWARE_DATETIME_2,
                (_OFFSET, _AWARE_DATETIME_1 + _OFFSET / 2),
            ),
            (
                _AWARE_DATETIME_2,
                _NAIVE_DATETIME_1,
                TypeError,
            ),
            (
                _AWARE_DATETIME_2,
                _NAIVE_DATETIME_2,
                TypeError,
            ),
            (
                _AWARE_DATETIME_2,
                _AWARE_DATETIME_1,
                (-_OFFSET, _AWARE_DATETIME_1 + _OFFSET / 2),
            ),
            (
                _AWARE_DATETIME_2,
                _AWARE_DATETIME_2,
                (datetime.timedelta(), _AWARE_DATETIME_2),
            ),
            (
                _AWARE_DATETIME_1.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                _AWARE_DATETIME_2.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                (_OFFSET, _AWARE_DATETIME_1 + _OFFSET / 2),
            ),
            (
                _AWARE_DATETIME_1.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                _AWARE_DATETIME_2,
                (_OFFSET, _AWARE_DATETIME_1 + _OFFSET / 2),
            ),
            (
                _AWARE_DATETIME_1,
                _AWARE_DATETIME_2.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                (_OFFSET, _AWARE_DATETIME_1 + _OFFSET / 2),
            ),
        ],
    )
    def test_init_and_properties(
        self,
        start,
        end,
        expected,
    ) -> None:
        period = peprock.dt.Period(start=start, end=end)
        assert period.start is start
        assert period.end is end

        match expected:
            case (duration, midpoint):
                assert period.duration == duration
                assert period.midpoint == midpoint
            case _:
                with pytest.raises(expected):
                    assert period.duration
                with pytest.raises(expected):
                    assert period.midpoint

    @pytest.mark.parametrize(
        ("item", "period", "expected"),
        [
            (
                _OFFSET,
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_1,
                ),
                TypeError,
            ),
            (
                _NAIVE_DATETIME_1 - _OFFSET,
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_1,
                ),
                False,
            ),
            (
                _NAIVE_DATETIME_1,
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_1,
                ),
                True,
            ),
            (
                _NAIVE_DATETIME_2,
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_1,
                ),
                False,
            ),
            (
                _NAIVE_DATETIME_1 - _OFFSET,
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                False,
            ),
            (
                _NAIVE_DATETIME_1,
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                True,
            ),
            (
                _NAIVE_DATETIME_2,
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                True,
            ),
            (
                _NAIVE_DATETIME_2 + _OFFSET,
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                False,
            ),
            (
                _AWARE_DATETIME_1,
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                TypeError,
            ),
            (
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1 - _OFFSET,
                    end=_NAIVE_DATETIME_1,
                ),
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_1,
                ),
                False,
            ),
            (
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_1,
                ),
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_1,
                ),
                True,
            ),
            (
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_1,
                ),
                False,
            ),
            (
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1 - _OFFSET,
                    end=_NAIVE_DATETIME_1,
                ),
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                False,
            ),
            (
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_1,
                ),
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                True,
            ),
            (
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                True,
            ),
            (
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2 + _OFFSET,
                ),
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                False,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                TypeError,
            ),
            (
                _AWARE_DATETIME_1 - _OFFSET,
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_1,
                ),
                False,
            ),
            (
                _AWARE_DATETIME_1,
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_1,
                ),
                True,
            ),
            (
                _AWARE_DATETIME_2,
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_1,
                ),
                False,
            ),
            (
                _AWARE_DATETIME_1 - _OFFSET,
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                False,
            ),
            (
                _AWARE_DATETIME_1,
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                True,
            ),
            (
                _AWARE_DATETIME_2,
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                True,
            ),
            (
                _AWARE_DATETIME_2 + _OFFSET,
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                False,
            ),
            (
                _NAIVE_DATETIME_1,
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                TypeError,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1 - _OFFSET,
                    end=_AWARE_DATETIME_1,
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_1,
                ),
                False,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_1,
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_1,
                ),
                True,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_1,
                ),
                False,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1 - _OFFSET,
                    end=_AWARE_DATETIME_1,
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                False,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_1,
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                True,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                True,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2 + _OFFSET,
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                False,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                    end=_AWARE_DATETIME_2.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                True,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                    end=_AWARE_DATETIME_2.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                ),
                True,
            ),
            (
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                    end=_AWARE_DATETIME_2.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                    end=_AWARE_DATETIME_2.astimezone(_VARIABLE_OFFSET_ZONE_INFO),
                ),
                True,
            ),
            (
                peprock.dt.Period(
                    start=_NAIVE_DATETIME_1,
                    end=_NAIVE_DATETIME_2,
                ),
                peprock.dt.Period(
                    start=_AWARE_DATETIME_1,
                    end=_AWARE_DATETIME_2,
                ),
                TypeError,
            ),
        ],
    )
    def test_contains(self, item, period, expected) -> None:
        match expected:
            case bool():
                assert (item in period) is expected
            case _:
                with pytest.raises(expected):
                    assert item in period
