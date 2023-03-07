# ruff: noqa: SIM201, SIM202

import dataclasses
import decimal
import fractions

import pytest

import peprock.models


@pytest.fixture(
    scope="session",
    params=[
        0.0,
        12.0,
        -34567.89012,
    ],
)
def float_magnitude(request):
    return request.param


@pytest.fixture(
    scope="session",
    params=[
        int,
        float,
        decimal.Decimal,
        fractions.Fraction,
    ],
)
def magnitude(request, float_magnitude):
    if request.param is decimal.Decimal:
        return request.param(str(float_magnitude))

    return request.param(float_magnitude)


@pytest.fixture(
    scope="session",
    params=[
        peprock.models.MetricPrefix.NONE,
        peprock.models.MetricPrefix.mega,
        peprock.models.MetricPrefix.milli,
    ],
)
def prefix(request):
    return request.param


@pytest.fixture(
    scope="session",
    params=[
        None,
        peprock.models.Unit.one,
        peprock.models.Unit.watt,
        "pep",
    ],
)
def unit(request):
    return request.param


@pytest.fixture(scope="session")
def measurement(magnitude, prefix, unit):
    return peprock.models.Measurement(
        magnitude=magnitude,
        prefix=prefix,
        unit=unit,
    )


@pytest.fixture(scope="session")
def measurement_plus_one(measurement):
    return dataclasses.replace(
        measurement,
        magnitude=measurement.magnitude + 1,
    )


@pytest.fixture(scope="session")
def measurement_plus_one_prefix_shift_up(measurement_plus_one):
    return dataclasses.replace(
        measurement_plus_one,
        prefix=peprock.models.MetricPrefix(
            measurement_plus_one.prefix
            + (1 if measurement_plus_one.magnitude > 0 else -1) * 3,
        ),
    )


@pytest.fixture(scope="session")
def measurement_prefix_shift(measurement):
    return dataclasses.replace(
        measurement,
        prefix=peprock.models.MetricPrefix(measurement.prefix + 3),
    )


@pytest.fixture(scope="session")
def measurement_other_unit(measurement):
    return dataclasses.replace(
        measurement,
        unit=peprock.models.Unit.candela,
    )


def test_unit_symbol(unit):
    if unit is None or unit is peprock.models.Unit.one:
        expected = ""
    elif isinstance(unit, peprock.models.Unit):
        expected = unit.symbol
    else:
        expected = str(unit)
    assert peprock.models.Measurement(magnitude=0, unit=unit)._unit_symbol == expected


@pytest.mark.parametrize(
    "format_spec",
    [
        "",
        "e",
        "f",
        "g",
        "n",
    ],
)
def test_format(measurement, format_spec):
    if format_spec and isinstance(measurement.magnitude, fractions.Fraction):
        with pytest.raises(TypeError):
            format(measurement, format_spec)
    else:
        formatted = format(measurement.magnitude, format_spec)
        if measurement.prefix.symbol or measurement._unit_symbol:
            formatted += f" {measurement.prefix.symbol}{measurement._unit_symbol}"
        assert format(measurement, format_spec) == formatted


def test_str(measurement):
    assert str(measurement) == format(measurement)


@pytest.mark.parametrize(
    ("measurement", "other", "expected"),
    [
        (
            peprock.models.Measurement(
                magnitude=12,
            ),
            peprock.models.Measurement(
                magnitude=34,
            ),
            (peprock.models.MetricPrefix.NONE, 12, 34),
        ),
        (
            peprock.models.Measurement(
                magnitude=12,
            ),
            peprock.models.Measurement(
                magnitude=34,
                prefix=peprock.models.MetricPrefix.milli,
            ),
            (peprock.models.MetricPrefix.milli, 12_000, 34),
        ),
        (
            peprock.models.Measurement(
                magnitude=12,
            ),
            peprock.models.Measurement(
                magnitude=34,
                prefix=peprock.models.MetricPrefix.kilo,
            ),
            (peprock.models.MetricPrefix.NONE, 12, 34_000),
        ),
        (
            peprock.models.Measurement(
                magnitude=12,
                prefix=peprock.models.MetricPrefix.mega,
            ),
            peprock.models.Measurement(
                magnitude=34,
                prefix=peprock.models.MetricPrefix.kilo,
            ),
            (peprock.models.MetricPrefix.kilo, 12_000, 34),
        ),
        (
            peprock.models.Measurement(
                magnitude=12.3,
                prefix=peprock.models.MetricPrefix.mega,
            ),
            peprock.models.Measurement(
                magnitude=34.5,
                prefix=peprock.models.MetricPrefix.kilo,
            ),
            (peprock.models.MetricPrefix.kilo, 12_300.0, 34.5),
        ),
        (
            peprock.models.Measurement(
                magnitude=decimal.Decimal("12.3"),
                prefix=peprock.models.MetricPrefix.mega,
            ),
            peprock.models.Measurement(
                magnitude=decimal.Decimal("34.5"),
                prefix=peprock.models.MetricPrefix.kilo,
            ),
            (
                peprock.models.MetricPrefix.kilo,
                decimal.Decimal("12300.0"),
                decimal.Decimal("34.5"),
            ),
        ),
        (
            peprock.models.Measurement(
                magnitude=fractions.Fraction("12.3"),
                prefix=peprock.models.MetricPrefix.mega,
            ),
            peprock.models.Measurement(
                magnitude=fractions.Fraction("34.5"),
                prefix=peprock.models.MetricPrefix.kilo,
            ),
            (
                peprock.models.MetricPrefix.kilo,
                fractions.Fraction("12300"),
                fractions.Fraction("34.5"),
            ),
        ),
    ],
    ids=lambda p: None if isinstance(p, tuple) else str(p),
)
def test_normalize_magnitudes(measurement, other, expected):
    assert measurement._normalize_magnitudes(other) == expected


def test_lt(
    measurement,
    measurement_plus_one,
    measurement_plus_one_prefix_shift_up,
    measurement_other_unit,
):
    assert not measurement < measurement
    assert measurement < measurement_plus_one
    assert measurement < measurement_plus_one_prefix_shift_up
    with pytest.raises(TypeError):
        assert measurement < measurement_other_unit

    assert not measurement_plus_one < measurement
    assert not measurement_plus_one < measurement_plus_one
    assert measurement_plus_one < measurement_plus_one_prefix_shift_up
    with pytest.raises(TypeError):
        assert measurement_plus_one < measurement_other_unit

    assert not measurement_plus_one_prefix_shift_up < measurement
    assert not measurement_plus_one_prefix_shift_up < measurement_plus_one
    assert (
        not measurement_plus_one_prefix_shift_up < measurement_plus_one_prefix_shift_up
    )
    with pytest.raises(TypeError):
        assert measurement_plus_one_prefix_shift_up < measurement_other_unit

    with pytest.raises(TypeError):
        assert measurement_other_unit < measurement
    with pytest.raises(TypeError):
        assert measurement_other_unit < measurement_plus_one
    with pytest.raises(TypeError):
        assert measurement_other_unit < measurement_plus_one_prefix_shift_up
    assert not measurement_other_unit < measurement_other_unit


def test_le(
    measurement,
    measurement_plus_one,
    measurement_plus_one_prefix_shift_up,
    measurement_other_unit,
):
    assert measurement <= measurement
    assert measurement <= measurement_plus_one
    assert measurement <= measurement_plus_one_prefix_shift_up
    with pytest.raises(TypeError):
        assert measurement <= measurement_other_unit

    assert not measurement_plus_one <= measurement
    assert measurement_plus_one <= measurement_plus_one
    assert measurement_plus_one <= measurement_plus_one_prefix_shift_up
    with pytest.raises(TypeError):
        assert measurement_plus_one <= measurement_other_unit

    assert not measurement_plus_one_prefix_shift_up <= measurement
    assert not measurement_plus_one_prefix_shift_up <= measurement_plus_one
    assert measurement_plus_one_prefix_shift_up <= measurement_plus_one_prefix_shift_up
    with pytest.raises(TypeError):
        assert measurement_plus_one_prefix_shift_up <= measurement_other_unit

    with pytest.raises(TypeError):
        assert measurement_other_unit <= measurement
    with pytest.raises(TypeError):
        assert measurement_other_unit <= measurement_plus_one
    with pytest.raises(TypeError):
        assert measurement_other_unit <= measurement_plus_one_prefix_shift_up
    assert measurement_other_unit <= measurement_other_unit


def test_eq(
    measurement,
    measurement_plus_one,
    measurement_plus_one_prefix_shift_up,
    measurement_other_unit,
):
    assert measurement == measurement
    assert not measurement == measurement_plus_one
    assert not measurement == measurement_plus_one_prefix_shift_up
    assert not measurement == measurement_other_unit

    assert not measurement_plus_one == measurement
    assert measurement_plus_one == measurement_plus_one
    assert not measurement_plus_one == measurement_plus_one_prefix_shift_up
    assert not measurement_plus_one == measurement_other_unit

    assert not measurement_plus_one_prefix_shift_up == measurement
    assert not measurement_plus_one_prefix_shift_up == measurement_plus_one
    assert measurement_plus_one_prefix_shift_up == measurement_plus_one_prefix_shift_up
    assert not measurement_plus_one_prefix_shift_up == measurement_other_unit

    assert not measurement_other_unit == measurement
    assert not measurement_other_unit == measurement_plus_one
    assert not measurement_other_unit == measurement_plus_one_prefix_shift_up
    assert measurement_other_unit == measurement_other_unit


def test_ne(
    measurement,
    measurement_plus_one,
    measurement_plus_one_prefix_shift_up,
    measurement_other_unit,
):
    assert not measurement != measurement
    assert measurement != measurement_plus_one
    assert measurement != measurement_plus_one_prefix_shift_up
    assert measurement != measurement_other_unit

    assert measurement_plus_one != measurement
    assert not measurement_plus_one != measurement_plus_one
    assert measurement_plus_one != measurement_plus_one_prefix_shift_up
    assert measurement_plus_one != measurement_other_unit

    assert measurement_plus_one_prefix_shift_up != measurement
    assert measurement_plus_one_prefix_shift_up != measurement_plus_one
    assert (
        not measurement_plus_one_prefix_shift_up != measurement_plus_one_prefix_shift_up
    )
    assert measurement_plus_one_prefix_shift_up != measurement_other_unit

    assert measurement_other_unit != measurement
    assert measurement_other_unit != measurement_plus_one
    assert measurement_other_unit != measurement_plus_one_prefix_shift_up
    assert not measurement_other_unit != measurement_other_unit


def test_gt(
    measurement,
    measurement_plus_one,
    measurement_plus_one_prefix_shift_up,
    measurement_other_unit,
):
    assert not measurement > measurement
    assert not measurement > measurement_plus_one
    assert not measurement > measurement_plus_one_prefix_shift_up
    with pytest.raises(TypeError):
        assert measurement > measurement_other_unit

    assert measurement_plus_one > measurement
    assert not measurement_plus_one > measurement_plus_one
    assert not measurement_plus_one > measurement_plus_one_prefix_shift_up
    with pytest.raises(TypeError):
        assert measurement_plus_one > measurement_other_unit

    assert measurement_plus_one_prefix_shift_up > measurement
    assert measurement_plus_one_prefix_shift_up > measurement_plus_one
    assert (
        not measurement_plus_one_prefix_shift_up > measurement_plus_one_prefix_shift_up
    )
    with pytest.raises(TypeError):
        assert measurement_plus_one_prefix_shift_up > measurement_other_unit

    with pytest.raises(TypeError):
        assert measurement_other_unit > measurement
    with pytest.raises(TypeError):
        assert measurement_other_unit > measurement_plus_one
    with pytest.raises(TypeError):
        assert measurement_other_unit > measurement_plus_one_prefix_shift_up
    assert not measurement_other_unit > measurement_other_unit


def test_ge(
    measurement,
    measurement_plus_one,
    measurement_plus_one_prefix_shift_up,
    measurement_other_unit,
):
    assert measurement >= measurement
    assert not measurement >= measurement_plus_one
    assert not measurement >= measurement_plus_one_prefix_shift_up
    with pytest.raises(TypeError):
        assert measurement >= measurement_other_unit

    assert measurement_plus_one >= measurement
    assert measurement_plus_one >= measurement_plus_one
    assert not measurement_plus_one >= measurement_plus_one_prefix_shift_up
    with pytest.raises(TypeError):
        assert measurement_plus_one >= measurement_other_unit

    assert measurement_plus_one_prefix_shift_up >= measurement
    assert measurement_plus_one_prefix_shift_up >= measurement_plus_one
    assert measurement_plus_one_prefix_shift_up >= measurement_plus_one_prefix_shift_up
    with pytest.raises(TypeError):
        assert measurement_plus_one_prefix_shift_up >= measurement_other_unit

    with pytest.raises(TypeError):
        assert measurement_other_unit >= measurement
    with pytest.raises(TypeError):
        assert measurement_other_unit >= measurement_plus_one
    with pytest.raises(TypeError):
        assert measurement_other_unit >= measurement_plus_one_prefix_shift_up
    assert measurement_other_unit >= measurement_other_unit


def test_hash(
    measurement,
    measurement_plus_one,
    measurement_plus_one_prefix_shift_up,
    measurement_other_unit,
):
    assert hash(measurement) == hash(measurement)
    assert hash(measurement) != hash(measurement_plus_one)
    assert hash(measurement) != hash(measurement_plus_one_prefix_shift_up)
    assert hash(measurement) != hash(measurement_other_unit)
    assert hash(measurement_plus_one) == hash(measurement_plus_one)
    assert hash(measurement_plus_one) != hash(measurement_plus_one_prefix_shift_up)
    assert hash(measurement_plus_one) != hash(measurement_other_unit)
    assert hash(measurement_plus_one_prefix_shift_up) == hash(
        measurement_plus_one_prefix_shift_up,
    )
    assert hash(measurement_plus_one_prefix_shift_up) != hash(measurement_other_unit)
    assert hash(measurement_other_unit) == hash(measurement_other_unit)

    measurement_copy = dataclasses.replace(measurement)
    assert measurement is not measurement_copy
    assert hash(measurement) == hash(measurement_copy)


def test_abs(measurement):
    measurement_abs = abs(measurement)
    assert measurement_abs.magnitude == abs(measurement.magnitude)
    assert measurement_abs.prefix == measurement.prefix
    assert measurement_abs.unit == measurement.unit


def test_add(
    measurement,
    measurement_plus_one,
    measurement_prefix_shift,
    measurement_other_unit,
):
    # combine measurement with self
    expected = dataclasses.replace(
        measurement,
        magnitude=measurement.magnitude + measurement.magnitude,
    )
    assert measurement + measurement == expected

    # combine measurement with measurement_plus_one
    expected = dataclasses.replace(
        measurement,
        magnitude=measurement.magnitude + measurement_plus_one.magnitude,
    )
    assert measurement + measurement_plus_one == expected
    assert measurement_plus_one + measurement == expected

    # combine measurement with measurement_prefix_shift
    expected = dataclasses.replace(
        measurement,
        magnitude=measurement.magnitude + measurement_prefix_shift.magnitude * 1000,
    )
    assert measurement + measurement_prefix_shift == expected
    assert measurement_prefix_shift + measurement == expected

    # combine measurement with measurement_other_unit
    with pytest.raises(TypeError):
        measurement + measurement_other_unit
    with pytest.raises(TypeError):
        measurement_other_unit + measurement


def test_floordiv(
    measurement,
    measurement_plus_one,
    measurement_prefix_shift,
    measurement_other_unit,
):
    # combine measurement with integer
    other = 32
    assert measurement // other == dataclasses.replace(
        measurement,
        magnitude=measurement.magnitude // other,
    )

    # combine measurement with float
    other = 32.1
    if isinstance(measurement.magnitude, decimal.Decimal):
        with pytest.raises(TypeError):
            measurement // other
    else:
        assert measurement // other == dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude // other,
        )

    # combine measurement with Decimal
    other = decimal.Decimal("32.1")
    if isinstance(measurement.magnitude, float | fractions.Fraction):
        with pytest.raises(TypeError):
            measurement // other
    else:
        assert measurement // other == dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude // other,
        )

    # combine measurement with Fraction
    other = fractions.Fraction(32.1)
    if isinstance(measurement.magnitude, decimal.Decimal):
        with pytest.raises(TypeError):
            measurement // other
    else:
        assert measurement // other == dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude // other,
        )

    # combine measurement with self
    if measurement.magnitude:
        assert measurement // measurement == 1
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement // measurement

    # combine measurement with measurement_plus_one
    if measurement_plus_one.magnitude:
        assert (
            measurement // measurement_plus_one
            == measurement.magnitude // measurement_plus_one.magnitude
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement // measurement_plus_one
    if measurement.magnitude:
        assert (
            measurement_plus_one // measurement
            == measurement_plus_one.magnitude // measurement.magnitude
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement_plus_one // measurement

    # combine measurement with measurement_prefix_shift
    if measurement_prefix_shift.magnitude:
        assert measurement // measurement_prefix_shift == measurement.magnitude // (
            measurement_prefix_shift.magnitude * 1000
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement // measurement_prefix_shift
    if measurement.magnitude:
        assert (
            measurement_prefix_shift // measurement
            == (measurement_prefix_shift.magnitude * 1000) // measurement.magnitude
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement_prefix_shift // measurement

    # combine measurement with measurement_other_unit
    with pytest.raises(TypeError):
        measurement // measurement_other_unit
    with pytest.raises(TypeError):
        measurement_other_unit // measurement


def test_mod(
    measurement,
    measurement_plus_one,
    measurement_prefix_shift,
    measurement_other_unit,
):
    # combine measurement with self
    if measurement.magnitude:
        assert measurement % measurement == dataclasses.replace(
            measurement,
            magnitude=0,
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement % measurement

    # combine measurement with measurement_plus_one
    if measurement_plus_one.magnitude:
        assert measurement % measurement_plus_one == dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude % measurement_plus_one.magnitude,
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement % measurement_plus_one
    if measurement.magnitude:
        assert measurement_plus_one % measurement == dataclasses.replace(
            measurement,
            magnitude=measurement_plus_one.magnitude % measurement.magnitude,
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement_plus_one % measurement

    # combine measurement with measurement_prefix_shift
    if measurement_prefix_shift.magnitude:
        assert measurement % measurement_prefix_shift == dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude
            % (measurement_prefix_shift.magnitude * 1000),
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement % measurement_prefix_shift
    if measurement.magnitude:
        assert measurement_prefix_shift % measurement == dataclasses.replace(
            measurement,
            magnitude=(measurement_prefix_shift.magnitude * 1000)
            % measurement.magnitude,
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement_prefix_shift % measurement

    # combine measurement with measurement_other_unit
    with pytest.raises(TypeError):
        measurement % measurement_other_unit
    with pytest.raises(TypeError):
        measurement_other_unit % measurement


def test_mul(measurement):
    # combine measurement with integer
    other = 32
    expected = dataclasses.replace(
        measurement,
        magnitude=measurement.magnitude * other,
    )
    assert measurement * other == expected
    assert other * measurement == expected

    # combine measurement with float
    other = 32.1
    if isinstance(measurement.magnitude, decimal.Decimal):
        with pytest.raises(TypeError):
            measurement * other
        with pytest.raises(TypeError):
            other * measurement
    else:
        expected = dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude * other,
        )
        assert measurement * other == expected
        assert other * measurement == expected

    # combine measurement with Decimal
    other = decimal.Decimal("32.1")
    if isinstance(measurement.magnitude, float | fractions.Fraction):
        with pytest.raises(TypeError):
            measurement * other
        with pytest.raises(TypeError):
            other * measurement
    else:
        expected = dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude * other,
        )
        assert measurement * other == expected
        assert other * measurement == expected

    # combine measurement with Fraction
    other = fractions.Fraction(32.1)
    if isinstance(measurement.magnitude, decimal.Decimal):
        with pytest.raises(TypeError):
            measurement * other
        with pytest.raises(TypeError):
            other * measurement
    else:
        expected = dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude * other,
        )
        assert measurement * other == expected
        assert other * measurement == expected

    # combine measurement with self
    with pytest.raises(TypeError):
        measurement * measurement


def test_neg(measurement):
    measurement_neg = -measurement
    assert measurement_neg.magnitude == -measurement.magnitude
    assert measurement_neg.prefix == measurement.prefix
    assert measurement_neg.unit == measurement.unit


def test_pos(measurement):
    measurement_pos = +measurement
    assert measurement_pos.magnitude == +measurement.magnitude
    assert measurement_pos.prefix == measurement.prefix
    assert measurement_pos.unit == measurement.unit


def test_sub(
    measurement,
    measurement_plus_one,
    measurement_prefix_shift,
    measurement_other_unit,
):
    # combine measurement with self
    assert measurement - measurement == dataclasses.replace(
        measurement,
        magnitude=measurement.magnitude - measurement.magnitude,
    )

    # combine measurement with measurement_plus_one
    assert measurement - measurement_plus_one == dataclasses.replace(
        measurement,
        magnitude=measurement.magnitude - measurement_plus_one.magnitude,
    )
    assert measurement_plus_one - measurement == dataclasses.replace(
        measurement,
        magnitude=measurement_plus_one.magnitude - measurement.magnitude,
    )

    # combine measurement with measurement_prefix_shift
    assert measurement - measurement_prefix_shift == dataclasses.replace(
        measurement,
        magnitude=measurement.magnitude - measurement_prefix_shift.magnitude * 1000,
    )
    assert measurement_prefix_shift - measurement == dataclasses.replace(
        measurement,
        magnitude=measurement_prefix_shift.magnitude * 1000 - measurement.magnitude,
    )

    # combine measurement with measurement_other_unit
    with pytest.raises(TypeError):
        measurement - measurement_other_unit
    with pytest.raises(TypeError):
        measurement_other_unit - measurement


def test_truediv(
    measurement,
    measurement_plus_one,
    measurement_prefix_shift,
    measurement_other_unit,
):
    # combine measurement with integer
    other = 32
    assert measurement / other == dataclasses.replace(
        measurement,
        magnitude=measurement.magnitude / other,
    )

    # combine measurement with float
    other = 32.1
    if isinstance(measurement.magnitude, decimal.Decimal):
        with pytest.raises(TypeError):
            measurement / other
    else:
        assert measurement / other == dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude / other,
        )

    # combine measurement with Decimal
    other = decimal.Decimal("32.1")
    if isinstance(measurement.magnitude, float | fractions.Fraction):
        with pytest.raises(TypeError):
            measurement / other
    else:
        assert measurement / other == dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude / other,
        )

    # combine measurement with Fraction
    other = fractions.Fraction(32.1)
    if isinstance(measurement.magnitude, decimal.Decimal):
        with pytest.raises(TypeError):
            measurement / other
    else:
        assert measurement / other == dataclasses.replace(
            measurement,
            magnitude=measurement.magnitude / other,
        )

    # combine measurement with self
    if measurement.magnitude:
        assert measurement / measurement == 1
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement / measurement

    # combine measurement with measurement_plus_one
    if measurement_plus_one.magnitude:
        assert (
            measurement / measurement_plus_one
            == measurement.magnitude / measurement_plus_one.magnitude
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement / measurement_plus_one
    if measurement.magnitude:
        assert (
            measurement_plus_one / measurement
            == measurement_plus_one.magnitude / measurement.magnitude
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement_plus_one / measurement

    # combine measurement with measurement_prefix_shift
    if measurement_prefix_shift.magnitude:
        assert measurement / measurement_prefix_shift == measurement.magnitude / (
            measurement_prefix_shift.magnitude * 1000
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement / measurement_prefix_shift
    if measurement.magnitude:
        assert (
            measurement_prefix_shift / measurement
            == (measurement_prefix_shift.magnitude * 1000) / measurement.magnitude
        )
    else:
        # noinspection PyTypeChecker
        with pytest.raises((ZeroDivisionError, decimal.InvalidOperation)):
            measurement_prefix_shift / measurement

    # combine measurement with measurement_other_unit
    with pytest.raises(TypeError):
        measurement / measurement_other_unit
    with pytest.raises(TypeError):
        measurement_other_unit / measurement


def test_bool(measurement):
    assert bool(measurement) is bool(measurement.magnitude)


@pytest.mark.parametrize(
    "ndigits",
    [
        None,
        1,
        -2,
    ],
)
def test_round(measurement, ndigits):
    assert round(measurement, ndigits) == dataclasses.replace(
        measurement,
        magnitude=round(measurement.magnitude, ndigits),
    )
