import decimal

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
    metric_filter = peprock.models.MetricPrefix[name]
    assert metric_filter == metric_filter.value == value
    assert metric_filter.symbol == symbol


@pytest.mark.parametrize(
    "metric_filter",
    list(peprock.models.MetricPrefix),
)
def test_from_symbol(metric_filter):
    assert (
        peprock.models.MetricPrefix.from_symbol(metric_filter.symbol) is metric_filter
    )


@pytest.mark.parametrize(
    "metric_filter",
    list(peprock.models.MetricPrefix),
)
def test_str(metric_filter):
    assert str(metric_filter) == metric_filter.symbol


@pytest.mark.parametrize(
    "other",
    list(peprock.models.MetricPrefix),
)
@pytest.mark.parametrize(
    "metric_filter",
    list(peprock.models.MetricPrefix),
)
def test_to(metric_filter, other):
    assert metric_filter.to(other) == pytest.approx(10 ** (metric_filter - other))


@pytest.mark.parametrize(
    "value",
    [
        -12,
        0,
        13,
        -2.34,
        0.0,
        53.433,
        decimal.Decimal("-12.4"),
        decimal.Decimal("-8"),
        decimal.Decimal("0"),
        decimal.Decimal("0.0"),
        decimal.Decimal("5.76"),
        decimal.Decimal("35"),
    ],
    ids=str,
)
@pytest.mark.parametrize(
    "to",
    [
        peprock.models.MetricPrefix.centi,
        peprock.models.MetricPrefix.NONE,
        peprock.models.MetricPrefix.mega,
    ],
)
@pytest.mark.parametrize(
    "metric_filter",
    [
        peprock.models.MetricPrefix.centi,
        peprock.models.MetricPrefix.NONE,
        peprock.models.MetricPrefix.mega,
    ],
)
def test_convert(metric_filter, to, value):
    assert metric_filter.convert(value, to) == pytest.approx(
        float(value) * metric_filter.to(to),
    )
