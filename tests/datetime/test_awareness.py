# ruff: noqa: FBT003

import datetime
import re
import typing
import zoneinfo

import pytest

import peprock.datetime

_DATE: typing.Final[datetime.date] = datetime.date(
    year=2023,
    month=2,
    day=24,
)
_TIME: typing.Final[datetime.time] = datetime.time(
    hour=1,
    minute=2,
    second=3,
    microsecond=4,
)
_DATETIME: typing.Final[datetime.datetime] = datetime.datetime.combine(
    date=_DATE,
    time=_TIME,
)

_UTC_TZINFO: typing.Final[datetime.tzinfo] = datetime.timezone.utc
_FIXED_OFFSET_ZONE_INFO: typing.Final[zoneinfo.ZoneInfo] = zoneinfo.ZoneInfo(
    "Etc/GMT+10",
)
_VARIABLE_OFFSET_ZONE_INFO: typing.Final[zoneinfo.ZoneInfo] = zoneinfo.ZoneInfo(
    "Europe/Paris",
)

_ZONE_INFOS: typing.Final[tuple[datetime.tzinfo, ...]] = (
    _UTC_TZINFO,
    _FIXED_OFFSET_ZONE_INFO,
    _VARIABLE_OFFSET_ZONE_INFO,
)


@pytest.mark.parametrize(
    ("arg", "is_naive"),
    [
        pytest.param(
            _DATE,
            True,
            id="date",
        ),
        pytest.param(
            _DATETIME,
            True,
            id="naive datetime",
        ),
        pytest.param(
            _DATETIME.replace(tzinfo=_UTC_TZINFO),
            False,
            id=f"aware datetime ({_UTC_TZINFO})",
        ),
        pytest.param(
            _DATETIME.replace(tzinfo=_FIXED_OFFSET_ZONE_INFO),
            False,
            id=f"aware datetime ({_FIXED_OFFSET_ZONE_INFO})",
        ),
        pytest.param(
            _DATETIME.replace(tzinfo=_VARIABLE_OFFSET_ZONE_INFO),
            False,
            id=f"aware datetime ({_VARIABLE_OFFSET_ZONE_INFO})",
        ),
        pytest.param(
            _TIME,
            True,
            id="naive time",
        ),
        pytest.param(
            _TIME.replace(tzinfo=_UTC_TZINFO),
            False,
            id=f"aware time ({_UTC_TZINFO})",
        ),
        pytest.param(
            _TIME.replace(tzinfo=_FIXED_OFFSET_ZONE_INFO),
            False,
            id=f"aware time ({_FIXED_OFFSET_ZONE_INFO})",
        ),
        pytest.param(
            _TIME.replace(tzinfo=_VARIABLE_OFFSET_ZONE_INFO),
            True,
            id=f"aware time ({_VARIABLE_OFFSET_ZONE_INFO})",
        ),
        pytest.param(
            1234,
            None,
            id="int",
        ),
        pytest.param(
            {"test": 1234},
            None,
            id="dict",
        ),
    ],
)
def test_is_naive_is_aware(arg: typing.Any, is_naive: bool | None) -> None:
    match is_naive:
        case None:
            match: str = (
                "^"
                + re.escape(
                    f"expected datetime.date | datetime.time | datetime.datetime, got {arg}",
                )
                + "$"
            )
            with pytest.raises(TypeError, match=match):
                peprock.datetime.is_naive(arg)
            with pytest.raises(TypeError, match=match):
                peprock.datetime.is_aware(arg)
        case _:
            assert peprock.datetime.is_naive(arg) == is_naive
            assert peprock.datetime.is_aware(arg) != is_naive


@pytest.mark.parametrize(
    "target_tz",
    [None, *(pytest.param(tzinfo, id=str(tzinfo)) for tzinfo in _ZONE_INFOS)],
)
@pytest.mark.parametrize(
    "assumed_tz",
    [None, *(pytest.param(tzinfo, id=str(tzinfo)) for tzinfo in _ZONE_INFOS)],
)
@pytest.mark.parametrize(
    "arg",
    [
        pytest.param(
            _DATETIME,
            id="naive datetime",
        ),
        *(
            pytest.param(
                _DATETIME.replace(tzinfo=tzinfo),
                id=f"aware datetime ({tzinfo})",
            )
            for tzinfo in _ZONE_INFOS
        ),
    ],
)
def test_ensure_aware_2(arg, assumed_tz, target_tz) -> None:
    if peprock.datetime.is_naive(arg) and assumed_tz is None:
        with pytest.raises(peprock.datetime.EnsureAwareError):
            peprock.datetime.ensure_aware(
                arg,
                assumed_tz=assumed_tz,
                target_tz=target_tz,
            )
    else:
        expected = arg
        if arg.tzinfo is None:
            expected = arg.replace(tzinfo=assumed_tz)
        if target_tz:
            expected = expected.astimezone(target_tz)
        assert (
            peprock.datetime.ensure_aware(
                arg,
                assumed_tz=assumed_tz,
                target_tz=target_tz,
            )
            == expected
        )
