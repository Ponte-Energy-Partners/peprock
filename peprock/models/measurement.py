"""Generic measurement model.

See https://en.wikipedia.org/wiki/Measurement

Examples
--------
>>> Measurement(1.2) + Measurement(4, MetricPrefix.kilo)
Measurement(magnitude=4001.2, prefix=<MetricPrefix.NONE: 0>, unit=None)

>>> str(abs(2 * Measurement(decimal.Decimal("-12.3"), MetricPrefix.mega, Unit.watt)))
'24.6 MW'
"""

from __future__ import annotations

import dataclasses
import decimal
import fractions
import functools
import typing

from .metric_prefix import MetricPrefix
from .unit import Unit

_MagnitudeT = typing.TypeVar(
    "_MagnitudeT",
    int,
    float,
    decimal.Decimal,
    fractions.Fraction,
)
_MagnitudeS = typing.TypeVar(
    "_MagnitudeS",
    int,
    float,
    decimal.Decimal,
    fractions.Fraction,
)


@dataclasses.dataclass(frozen=True)
class Measurement(
    typing.SupportsAbs["Measurement[_MagnitudeT]"],
    typing.Generic[_MagnitudeT],
):
    """Measurement model supporting conversion and arithmetic operations."""

    magnitude: _MagnitudeT
    prefix: MetricPrefix = MetricPrefix.NONE
    unit: Unit | str | None = None

    @functools.cached_property
    def _unit_symbol(self: Measurement) -> str:
        match self.unit:
            case None | Unit.one:
                return ""
            case Unit():
                return self.unit.symbol
            case _:
                return str(self.unit)

    def __format__(self: Measurement, format_spec: str) -> str:
        """Format measurement and return str."""
        formatted: str = format(self.magnitude, format_spec)
        if suffix := self.prefix.symbol + self._unit_symbol:
            return f"{formatted} {suffix}"
        return formatted

    @functools.cached_property
    def _str(self: Measurement) -> str:
        return format(self)

    def __str__(self: Measurement) -> str:
        """Return str(self)."""
        return self._str

    def _normalize_magnitudes(
        self: Measurement[_MagnitudeT],
        other: Measurement[_MagnitudeS],
        /,
    ) -> tuple[
        Measurement[_MagnitudeT] | Measurement[_MagnitudeS],
        _MagnitudeT | float,
        _MagnitudeS | float,
    ]:
        target: Measurement[_MagnitudeT] | Measurement[_MagnitudeS] = (
            self if self.prefix <= other.prefix else other
        )
        return (
            target,
            self.prefix.convert(self.magnitude, to=target.prefix),
            other.prefix.convert(other.magnitude, to=target.prefix),
        )

    def __lt__(self: Measurement, other: Measurement) -> bool:
        """Return self < other."""
        if isinstance(other, Measurement) and self.unit == other.unit:
            _, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return magnitude_self < magnitude_other

        return NotImplemented

    def __le__(self: Measurement, other: Measurement) -> bool:
        """Return self <= other."""
        if isinstance(other, Measurement) and self.unit == other.unit:
            _, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return magnitude_self <= magnitude_other

        return NotImplemented

    def __eq__(self: Measurement, other: object) -> bool:
        """Return self == other."""
        if isinstance(other, Measurement) and self.unit == other.unit:
            _, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return magnitude_self == magnitude_other

        return NotImplemented

    def __ne__(self: Measurement, other: object) -> bool:
        """Return self != other."""
        if isinstance(other, Measurement) and self.unit == other.unit:
            _, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return magnitude_self != magnitude_other

        return NotImplemented

    def __gt__(self: Measurement, other: Measurement) -> bool:
        """Return self > other."""
        if isinstance(other, Measurement) and self.unit == other.unit:
            _, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return magnitude_self > magnitude_other

        return NotImplemented

    def __ge__(self: Measurement, other: Measurement) -> bool:
        """Return self >= other."""
        if isinstance(other, Measurement) and self.unit == other.unit:
            _, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return magnitude_self >= magnitude_other

        return NotImplemented

    @functools.cached_property
    def _hash(self: Measurement) -> int:
        return hash(
            (
                self.prefix.convert(self.magnitude, to=MetricPrefix.NONE),
                self.unit,
            ),
        )

    def __hash__(self: Measurement) -> int:
        """Return hash(self)."""
        return self._hash

    def __abs__(self: _MeasurementT_co) -> _MeasurementT_co:
        """Return abs(self)."""
        return dataclasses.replace(
            self,
            magnitude=abs(self.magnitude),
        )

    @typing.overload
    def __add__(
        self: Measurement[int],
        other: Measurement[int],
    ) -> Measurement[int] | Measurement[float]:
        ...

    @typing.overload
    def __add__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: Measurement[float],
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __add__(
        self: Measurement[float],
        other: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __add__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __add__(
        self: Measurement[decimal.Decimal],
        other: Measurement[int] | Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __add__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]:
        ...

    @typing.overload
    def __add__(
        self: Measurement[fractions.Fraction],
        other: Measurement[int] | Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]:
        ...

    def __add__(self: Measurement, other: Measurement) -> Measurement:
        """Return self + other."""
        if isinstance(other, Measurement) and self.unit == other.unit:
            target, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return dataclasses.replace(
                target,
                magnitude=magnitude_self + magnitude_other,
            )

        return NotImplemented

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: int | fractions.Fraction,
    ) -> Measurement[int]:
        ...

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: float,
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __floordiv__(
        self: Measurement[float],
        other: int | float | fractions.Fraction,
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: decimal.Decimal,
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __floordiv__(
        self: Measurement[decimal.Decimal],
        other: int | decimal.Decimal,
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: Measurement[int] | Measurement[fractions.Fraction],
    ) -> int:
        ...

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: Measurement[float],
    ) -> float:
        ...

    @typing.overload
    def __floordiv__(
        self: Measurement[float],
        other: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
    ) -> float:
        ...

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: Measurement[decimal.Decimal],
    ) -> decimal.Decimal:
        ...

    @typing.overload
    def __floordiv__(
        self: Measurement[decimal.Decimal],
        other: Measurement[int] | Measurement[decimal.Decimal],
    ) -> decimal.Decimal:
        ...

    def __floordiv__(
        self: Measurement,
        other: int | float | decimal.Decimal | fractions.Fraction | Measurement,
    ) -> Measurement | int | float | decimal.Decimal:
        """Return self // other."""
        if isinstance(other, int | float | decimal.Decimal | fractions.Fraction):
            return dataclasses.replace(
                self,
                magnitude=self.magnitude // other,
            )

        if isinstance(other, Measurement) and self.unit == other.unit:
            _, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return magnitude_self // magnitude_other

        return NotImplemented

    @typing.overload
    def __mod__(
        self: Measurement[int],
        other: Measurement[int],
    ) -> Measurement[int]:
        ...

    @typing.overload
    def __mod__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: Measurement[float],
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __mod__(
        self: Measurement[float],
        other: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __mod__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __mod__(
        self: Measurement[decimal.Decimal],
        other: Measurement[int] | Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __mod__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]:
        ...

    @typing.overload
    def __mod__(
        self: Measurement[fractions.Fraction],
        other: Measurement[int] | Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]:
        ...

    def __mod__(
        self: Measurement,
        other: Measurement,
    ) -> Measurement:
        """Return self % other."""
        if isinstance(other, Measurement) and self.unit == other.unit:
            target, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return dataclasses.replace(
                target,
                magnitude=magnitude_self % magnitude_other,
            )

        return NotImplemented

    @typing.overload
    def __mul__(
        self: Measurement[int],
        other: int,
    ) -> Measurement[int]:
        ...

    @typing.overload
    def __mul__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: float,
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __mul__(
        self: Measurement[float],
        other: int | float | fractions.Fraction,
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __mul__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: decimal.Decimal,
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __mul__(
        self: Measurement[decimal.Decimal],
        other: int | decimal.Decimal,
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __mul__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: fractions.Fraction,
    ) -> Measurement[fractions.Fraction]:
        ...

    @typing.overload
    def __mul__(
        self: Measurement[fractions.Fraction],
        other: int | fractions.Fraction,
    ) -> Measurement[fractions.Fraction]:
        ...

    def __mul__(
        self: Measurement,
        other: int | float | decimal.Decimal | fractions.Fraction,
    ) -> Measurement:
        """Return self * other."""
        if isinstance(other, int | float | decimal.Decimal | fractions.Fraction):
            return dataclasses.replace(
                self,
                magnitude=self.magnitude * other,
            )

        return NotImplemented

    @typing.overload
    def __rmul__(
        self: Measurement[int],
        other: int,
    ) -> Measurement[int]:
        ...

    @typing.overload
    def __rmul__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: float,
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __rmul__(
        self: Measurement[float],
        other: int | float | fractions.Fraction,
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __rmul__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: decimal.Decimal,
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __rmul__(
        self: Measurement[decimal.Decimal],
        other: int | decimal.Decimal,
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __rmul__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: fractions.Fraction,
    ) -> Measurement[fractions.Fraction]:
        ...

    @typing.overload
    def __rmul__(
        self: Measurement[fractions.Fraction],
        other: int | fractions.Fraction,
    ) -> Measurement[fractions.Fraction]:
        ...

    def __rmul__(
        self: Measurement,
        other: int | float | decimal.Decimal | fractions.Fraction,
    ) -> Measurement:
        """Return other * self."""
        return self.__mul__(other)

    def __neg__(self: Measurement[_MagnitudeT]) -> Measurement[_MagnitudeT]:
        """Return -self."""
        return dataclasses.replace(
            self,
            magnitude=-self.magnitude,
        )

    def __pos__(self: Measurement[_MagnitudeT]) -> Measurement[_MagnitudeT]:
        """Return +self."""
        return dataclasses.replace(
            self,
            magnitude=+self.magnitude,
        )

    @typing.overload
    def __sub__(
        self: Measurement[int],
        other: Measurement[int],
    ) -> Measurement[int] | Measurement[float]:
        ...

    @typing.overload
    def __sub__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: Measurement[float],
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __sub__(
        self: Measurement[float],
        other: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __sub__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __sub__(
        self: Measurement[decimal.Decimal],
        other: Measurement[int] | Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __sub__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]:
        ...

    @typing.overload
    def __sub__(
        self: Measurement[fractions.Fraction],
        other: Measurement[int] | Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]:
        ...

    def __sub__(self: Measurement, other: Measurement) -> Measurement:
        """Return self - other."""
        if isinstance(other, Measurement) and self.unit == other.unit:
            target, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return dataclasses.replace(
                target,
                magnitude=magnitude_self - magnitude_other,
            )

        return NotImplemented

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[float],
        other: int | float,
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[float],
        other: fractions.Fraction,
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[fractions.Fraction],
        other: float,
    ) -> Measurement[float]:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: decimal.Decimal,
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[decimal.Decimal],
        other: int | decimal.Decimal,
    ) -> Measurement[decimal.Decimal]:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: fractions.Fraction,
    ) -> Measurement[fractions.Fraction]:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[fractions.Fraction],
        other: int | fractions.Fraction,
    ) -> Measurement[fractions.Fraction]:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[float],
        other: Measurement[int] | Measurement[float],
    ) -> float:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[float],
        other: Measurement[fractions.Fraction],
    ) -> float:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[fractions.Fraction],
        other: Measurement[float],
    ) -> float:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: Measurement[decimal.Decimal],
    ) -> decimal.Decimal:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[decimal.Decimal],
        other: Measurement[int] | Measurement[decimal.Decimal],
    ) -> decimal.Decimal:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: Measurement[fractions.Fraction],
    ) -> fractions.Fraction:
        ...

    @typing.overload
    def __truediv__(
        self: Measurement[fractions.Fraction],
        other: Measurement[int] | Measurement[fractions.Fraction],
    ) -> fractions.Fraction:
        ...

    def __truediv__(
        self: Measurement,
        other: int | float | decimal.Decimal | fractions.Fraction | Measurement,
    ) -> Measurement | float | decimal.Decimal | fractions.Fraction:
        """Return self / other."""
        if isinstance(other, int | float | decimal.Decimal | fractions.Fraction):
            return dataclasses.replace(
                self,
                magnitude=self.magnitude / other,
            )

        if isinstance(other, Measurement) and self.unit == other.unit:
            _, magnitude_self, magnitude_other = self._normalize_magnitudes(other)
            return magnitude_self / magnitude_other

        return NotImplemented

    def __bool__(self: Measurement) -> bool:
        """Return True if magnitude is nonzero; otherwise return False."""
        return bool(self.magnitude)

    @typing.overload
    def __round__(self: Measurement) -> Measurement[int]:
        ...

    @typing.overload
    def __round__(
        self: Measurement[_MagnitudeT],
        __ndigits: int,
    ) -> Measurement[_MagnitudeT]:
        ...

    def __round__(
        self: Measurement,
        __ndigits: int | None = None,
    ) -> Measurement:
        """Return round(self)."""
        return dataclasses.replace(
            self,
            magnitude=round(self.magnitude, __ndigits),
        )


_MeasurementT_co = typing.TypeVar("_MeasurementT_co", bound=Measurement, covariant=True)

__all__ = [
    "Measurement",
]
