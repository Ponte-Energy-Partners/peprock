import decimal
import fractions

import pytest

import peprock.models


@pytest.mark.parametrize(
    ("name", "value", "symbol"),
    [
        ("quetta", 30, "Q"),
        ("ronna", 27, "R"),
        ("yotta", 24, "Y"),
        ("zetta", 21, "Z"),
        ("exa", 18, "E"),
        ("peta", 15, "P"),
        ("tera", 12, "T"),
        ("giga", 9, "G"),
        ("mega", 6, "M"),
        ("kilo", 3, "k"),
        ("hecto", 2, "h"),
        ("deca", 1, "da"),
        ("NONE", 0, ""),
        ("deci", -1, "d"),
        ("centi", -2, "c"),
        ("milli", -3, "m"),
        ("micro", -6, "μ"),
        ("nano", -9, "n"),
        ("pico", -12, "p"),
        ("femto", -15, "f"),
        ("atto", -18, "a"),
        ("zepto", -21, "z"),
        ("yocto", -24, "y"),
        ("ronto", -27, "r"),
        ("quecto", -30, "q"),
    ],
    ids=lambda n, *_: n,
)
def test_members(name, value, symbol):
    metric_prefix = peprock.models.MetricPrefix[name]
    assert metric_prefix == metric_prefix.value == value
    assert metric_prefix.symbol == symbol


@pytest.mark.parametrize(
    "metric_prefix",
    list(peprock.models.MetricPrefix),
)
def test_from_symbol(metric_prefix):
    assert (
        peprock.models.MetricPrefix.from_symbol(metric_prefix.symbol) is metric_prefix
    )


@pytest.mark.parametrize(
    "metric_prefix",
    list(peprock.models.MetricPrefix),
)
def test_str(metric_prefix):
    assert str(metric_prefix) == metric_prefix.symbol


@pytest.mark.parametrize(
    "number_type",
    [
        int,
        float,
        complex,
        decimal.Decimal,
        fractions.Fraction,
    ],
)
@pytest.mark.parametrize(
    "other",
    list(peprock.models.MetricPrefix) + list(range(-6, 6, 2)),
)
@pytest.mark.parametrize(
    "metric_prefix",
    list(peprock.models.MetricPrefix),
)
def test_to(metric_prefix, other, number_type):
    assert metric_prefix.to(other, number_type=number_type) == pytest.approx(
        number_type(peprock.models.metric_prefix._BASE) ** (metric_prefix - other),
    )


@pytest.mark.parametrize(
    "value",
    [
        -12,
        0,
        13,
        -2.34,
        0.0,
        53.433,
        complex(1.23, 4.56),
        decimal.Decimal("-12.4"),
        decimal.Decimal("-8"),
        decimal.Decimal("0"),
        decimal.Decimal("0.0"),
        decimal.Decimal("5.76"),
        decimal.Decimal("35"),
        fractions.Fraction(12, 7),
    ],
    ids=str,
)
@pytest.mark.parametrize(
    "to",
    [
        None,
        peprock.models.MetricPrefix.centi,
        peprock.models.MetricPrefix.NONE,
        peprock.models.MetricPrefix.mega,
    ],
)
@pytest.mark.parametrize(
    "metric_prefix",
    [
        peprock.models.MetricPrefix.centi,
        peprock.models.MetricPrefix.NONE,
        peprock.models.MetricPrefix.mega,
    ],
)
def test_convert(metric_prefix, to, value):
    result = (
        metric_prefix.convert(value) if to is None else metric_prefix.convert(value, to)
    )

    assert result == pytest.approx(
        value
        * metric_prefix.to(
            to or peprock.models.MetricPrefix.NONE,
            number_type=type(value),
        ),
    )
