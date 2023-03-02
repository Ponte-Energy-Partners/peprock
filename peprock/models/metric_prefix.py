"""Metric prefix model.

See https://en.wikipedia.org/wiki/Metric_prefix
"""

from __future__ import annotations

import enum
import functools
import types
import typing

if typing.TYPE_CHECKING:
    import decimal
    import fractions

    ComplexT = typing.TypeVar(
        "ComplexT",
        float,
        complex,
        decimal.Decimal,
        fractions.Fraction,
    )

_BASE: typing.Final[int] = 10


class MetricPrefix(enum.IntEnum):
    """MetricPrefix IntEnum with symbol and conversion support."""

    quetta = 30
    ronna = 27
    yotta = 24
    zetta = 21
    exa = 18
    peta = 15
    tera = 12
    giga = 9
    mega = 6
    kilo = 3
    hecto = 2
    deca = 1
    NONE = 0
    deci = -1
    centi = -2
    milli = -3
    micro = -6
    nano = -9
    pico = -12
    femto = -15
    atto = -18
    zepto = -21
    yocto = -24
    ronto = -27
    quecto = -30

    @classmethod
    def from_symbol(cls: type[MetricPrefix], symbol: str, /) -> MetricPrefix:
        """Return MetricPrefix by symbol."""
        return cls._by_symbol()[symbol]

    @functools.cached_property
    def symbol(self: MetricPrefix) -> str:
        """Metric prefix symbol, e.g. G for giga."""
        return self._symbols()[self]

    def __str__(self: MetricPrefix) -> str:
        """Return symbol."""
        return self.symbol

    @typing.overload
    def to(
        self: MetricPrefix,
        other: MetricPrefix | int,
        /,
        *,
        number_type: type[int] = int,
    ) -> int | float:
        ...

    @typing.overload
    def to(
        self: MetricPrefix,
        other: MetricPrefix | int,
        /,
        *,
        number_type: type[ComplexT],
    ) -> ComplexT:
        ...

    def to(
        self: MetricPrefix,
        other: MetricPrefix | int,
        /,
        *,
        number_type: type[int | ComplexT] = int,
    ) -> int | ComplexT:
        """Calculate conversion factor between self and other."""
        return number_type(_BASE) ** (self - other)

    @typing.overload
    def convert(
        self: MetricPrefix,
        value: int,
        /,
        to: MetricPrefix,
    ) -> int | float:
        ...

    @typing.overload
    def convert(
        self: MetricPrefix,
        value: ComplexT,
        /,
        to: MetricPrefix,
    ) -> ComplexT:
        ...

    def convert(
        self,
        value,
        /,
        to,
    ):
        """Convert value from metric prefix self to to."""
        return value * self.to(to, number_type=type(value))

    @staticmethod
    @functools.cache
    def _symbols() -> types.MappingProxyType[MetricPrefix, str]:
        return types.MappingProxyType(
            {
                MetricPrefix.quetta: "Q",
                MetricPrefix.ronna: "R",
                MetricPrefix.yotta: "Y",
                MetricPrefix.zetta: "Z",
                MetricPrefix.exa: "E",
                MetricPrefix.peta: "P",
                MetricPrefix.tera: "T",
                MetricPrefix.giga: "G",
                MetricPrefix.mega: "M",
                MetricPrefix.kilo: "k",
                MetricPrefix.hecto: "h",
                MetricPrefix.deca: "da",
                MetricPrefix.NONE: "",
                MetricPrefix.deci: "d",
                MetricPrefix.centi: "c",
                MetricPrefix.milli: "m",
                MetricPrefix.micro: "μ",
                MetricPrefix.nano: "n",
                MetricPrefix.pico: "p",
                MetricPrefix.femto: "f",
                MetricPrefix.atto: "a",
                MetricPrefix.zepto: "z",
                MetricPrefix.yocto: "y",
                MetricPrefix.ronto: "r",
                MetricPrefix.quecto: "q",
            },
        )

    @classmethod
    @functools.cache
    def _by_symbol(
        cls: type[MetricPrefix],
    ) -> types.MappingProxyType[str, MetricPrefix]:
        return types.MappingProxyType(
            {symbol: metric_prefix for metric_prefix, symbol in cls._symbols().items()},
        )


__all__ = [
    "MetricPrefix",
]
