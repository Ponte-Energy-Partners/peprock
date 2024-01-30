"""Generic measurement model.

See https://en.wikipedia.org/wiki/Measurement

Examples
--------
>>> Measurement(1.2) + Measurement(4, MetricPrefix.kilo)
Measurement(magnitude=4001.2, prefix=<MetricPrefix.NONE: 0>, unit=None)

>>> str(abs(2 * Measurement(decimal.Decimal("-12.3"), MetricPrefix.mega, Unit.watt)))
'24.6 MW'

>>> int(Measurement(0.123456, MetricPrefix.kilo))
123


"""

from __future__ import annotations

import dataclasses
import decimal
import fractions
import functools
import operator
import typing

from .metric_prefix import MetricPrefix
from .unit import Unit

if typing.TYPE_CHECKING:
    import collections.abc
    import sys

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self


_T = typing.TypeVar("_T")
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
class Measurement(typing.Generic[_MagnitudeT]):
    """Measurement model supporting conversion and arithmetic operations."""

    magnitude: _MagnitudeT
    prefix: MetricPrefix = MetricPrefix.NONE
    unit: Unit | str | None = None

    @functools.cached_property
    def _unit_symbol(self: Self) -> str:
        match self.unit:
            case None | Unit.one:
                return ""
            case Unit():
                return self.unit.symbol
            case _:
                return self.unit

    def __format__(self: Self, format_spec: str) -> str:
        """Format measurement and return str."""
        if self.prefix.symbol or (self.unit and self.unit is not Unit.one):
            return (
                f"{self.magnitude:{format_spec}} "
                f"{self.prefix.symbol}{self._unit_symbol}"
            )

        return format(self.magnitude, format_spec)

    @functools.cached_property
    def _str(self: Self) -> str:
        return format(self)

    def __str__(self: Self) -> str:
        """Return str(self)."""
        return self._str

    @classmethod
    @functools.cache
    def _init_field_names(cls: type[Self]) -> tuple[str, ...]:
        return tuple(field.name for field in dataclasses.fields(cls) if field.init)

    def replace(self: Self, **changes: typing.Any) -> Self:
        """Return a new object replacing specified fields with new values."""
        return type(self)(
            **{
                field_name: (
                    changes[field_name]
                    if field_name in changes
                    else getattr(self, field_name)
                )
                for field_name in self._init_field_names()
            },
        )

    @typing.overload
    def _apply_operator(
        self: Self,
        __other: Measurement[_MagnitudeS],
        __operator: collections.abc.Callable[
            [_MagnitudeT | float, _MagnitudeS | float],
            _T,
        ],
        /,
        *,
        wrap_in_measurement: typing.Literal[False] = False,
    ) -> _T: ...

    @typing.overload
    def _apply_operator(
        self: Self,
        __other: object,
        __operator: collections.abc.Callable[[_MagnitudeT | float, object], _T],
        /,
        *,
        wrap_in_measurement: typing.Literal[False] = False,
    ) -> _T: ...

    @typing.overload
    def _apply_operator(
        self: Self,
        __other: Measurement[_MagnitudeS],
        __operator: collections.abc.Callable[
            [_MagnitudeT | float, _MagnitudeS | float],
            _T,
        ],
        /,
        *,
        wrap_in_measurement: typing.Literal[True],
    ) -> Self: ...

    def _apply_operator(  # noqa: PLR0911
        self,
        __other,
        __operator,
        /,
        *,
        wrap_in_measurement=False,
    ):
        if isinstance(__other, Measurement) and self.unit == __other.unit:
            if (diff := self.prefix - __other.prefix) == 0:
                magnitude = __operator(
                    self.magnitude,
                    __other.magnitude,
                )

                if wrap_in_measurement:
                    return self.replace(
                        magnitude=magnitude,
                    )

                return magnitude

            if diff < 0:
                magnitude = __operator(
                    self.magnitude,
                    __other.prefix.convert(__other.magnitude, to=self.prefix),
                )

                if wrap_in_measurement:
                    return self.replace(
                        magnitude=magnitude,
                    )

                return magnitude

            magnitude = __operator(
                self.prefix.convert(self.magnitude, to=__other.prefix),
                __other.magnitude,
            )

            if wrap_in_measurement:
                return self.replace(
                    magnitude=magnitude,
                    prefix=__other.prefix,
                )

            return magnitude

        return NotImplemented

    def __lt__(self: Self, other: Measurement) -> bool:
        """Return self < other."""
        return self._apply_operator(other, operator.lt)

    def __le__(self: Self, other: Measurement) -> bool:
        """Return self <= other."""
        return self._apply_operator(other, operator.le)

    def __eq__(self: Self, other: object) -> bool:
        """Return self == other."""
        return self._apply_operator(other, operator.eq)

    def __ne__(self: Self, other: object) -> bool:
        """Return self != other."""
        return self._apply_operator(other, operator.ne)

    def __gt__(self: Self, other: Measurement) -> bool:
        """Return self > other."""
        return self._apply_operator(other, operator.gt)

    def __ge__(self: Self, other: Measurement) -> bool:
        """Return self >= other."""
        return self._apply_operator(other, operator.ge)

    @functools.cached_property
    def _hash(self: Self) -> int:
        return hash((self.prefix.convert(self.magnitude), self.unit))

    def __hash__(self: Self) -> int:
        """Return hash(self)."""
        return self._hash

    def __abs__(self: Self) -> Self:
        """Return abs(self)."""
        return self.replace(
            magnitude=abs(self.magnitude),
        )

    @typing.overload
    def __add__(
        self: Measurement[int],
        other: Measurement[int],
    ) -> Measurement[int] | Measurement[float]: ...

    @typing.overload
    def __add__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: Measurement[float],
    ) -> Measurement[float]: ...

    @typing.overload
    def __add__(
        self: Measurement[float],
        other: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
    ) -> Measurement[float]: ...

    @typing.overload
    def __add__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __add__(
        self: Measurement[decimal.Decimal],
        other: Measurement[int] | Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __add__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]: ...

    @typing.overload
    def __add__(
        self: Measurement[fractions.Fraction],
        other: Measurement[int] | Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]: ...

    def __add__(self, other):
        """Return self + other."""
        return self._apply_operator(other, operator.add, wrap_in_measurement=True)

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: int | fractions.Fraction,
    ) -> Measurement[int]: ...

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: float,
    ) -> Measurement[float]: ...

    @typing.overload
    def __floordiv__(
        self: Measurement[float],
        other: float | fractions.Fraction,
    ) -> Measurement[float]: ...

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: decimal.Decimal,
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __floordiv__(
        self: Measurement[decimal.Decimal],
        other: int | decimal.Decimal,
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: Measurement[int] | Measurement[fractions.Fraction],
    ) -> int: ...

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: Measurement[float],
    ) -> float: ...

    @typing.overload
    def __floordiv__(
        self: Measurement[float],
        other: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
    ) -> float: ...

    @typing.overload
    def __floordiv__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: Measurement[decimal.Decimal],
    ) -> decimal.Decimal: ...

    @typing.overload
    def __floordiv__(
        self: Measurement[decimal.Decimal],
        other: Measurement[int] | Measurement[decimal.Decimal],
    ) -> decimal.Decimal: ...

    def __floordiv__(self, other):
        """Return self // other."""
        match other:
            case int() | float() | decimal.Decimal() | fractions.Fraction():
                return self.replace(
                    magnitude=self.magnitude // other,
                )

        return self._apply_operator(other, operator.floordiv)

    @typing.overload
    def __mod__(
        self: Measurement[int],
        other: Measurement[int],
    ) -> Measurement[int]: ...

    @typing.overload
    def __mod__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: Measurement[float],
    ) -> Measurement[float]: ...

    @typing.overload
    def __mod__(
        self: Measurement[float],
        other: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
    ) -> Measurement[float]: ...

    @typing.overload
    def __mod__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __mod__(
        self: Measurement[decimal.Decimal],
        other: Measurement[int] | Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __mod__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]: ...

    @typing.overload
    def __mod__(
        self: Measurement[fractions.Fraction],
        other: Measurement[int] | Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]: ...

    def __mod__(self, other):
        """Return self % other."""
        return self._apply_operator(other, operator.mod, wrap_in_measurement=True)

    @typing.overload
    def __mul__(
        self: Measurement[int],
        other: int,
    ) -> Measurement[int]: ...

    @typing.overload
    def __mul__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: float,
    ) -> Measurement[float]: ...

    @typing.overload
    def __mul__(
        self: Measurement[float],
        other: float | fractions.Fraction,
    ) -> Measurement[float]: ...

    @typing.overload
    def __mul__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: decimal.Decimal,
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __mul__(
        self: Measurement[decimal.Decimal],
        other: int | decimal.Decimal,
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __mul__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: fractions.Fraction,
    ) -> Measurement[fractions.Fraction]: ...

    @typing.overload
    def __mul__(
        self: Measurement[fractions.Fraction],
        other: int | fractions.Fraction,
    ) -> Measurement[fractions.Fraction]: ...

    def __mul__(self, other):
        """Return self * other."""
        match other:
            case int() | float() | decimal.Decimal() | fractions.Fraction():
                return self.replace(
                    magnitude=self.magnitude * other,
                )

        return NotImplemented

    @typing.overload
    def __rmul__(
        self: Measurement[int],
        other: int,
    ) -> Measurement[int]: ...

    @typing.overload
    def __rmul__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: float,
    ) -> Measurement[float]: ...

    @typing.overload
    def __rmul__(
        self: Measurement[float],
        other: float | fractions.Fraction,
    ) -> Measurement[float]: ...

    @typing.overload
    def __rmul__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: decimal.Decimal,
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __rmul__(
        self: Measurement[decimal.Decimal],
        other: int | decimal.Decimal,
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __rmul__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: fractions.Fraction,
    ) -> Measurement[fractions.Fraction]: ...

    @typing.overload
    def __rmul__(
        self: Measurement[fractions.Fraction],
        other: int | fractions.Fraction,
    ) -> Measurement[fractions.Fraction]: ...

    def __rmul__(self, other):
        """Return other * self."""
        return self.__mul__(other)

    def __neg__(self: Self) -> Self:
        """Return -self."""
        return self.replace(
            magnitude=-self.magnitude,
        )

    def __pos__(self: Self) -> Self:
        """Return +self."""
        return self.replace(
            magnitude=+self.magnitude,
        )

    @typing.overload
    def __sub__(
        self: Measurement[int],
        other: Measurement[int],
    ) -> Measurement[int] | Measurement[float]: ...

    @typing.overload
    def __sub__(
        self: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
        other: Measurement[float],
    ) -> Measurement[float]: ...

    @typing.overload
    def __sub__(
        self: Measurement[float],
        other: Measurement[int] | Measurement[float] | Measurement[fractions.Fraction],
    ) -> Measurement[float]: ...

    @typing.overload
    def __sub__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __sub__(
        self: Measurement[decimal.Decimal],
        other: Measurement[int] | Measurement[decimal.Decimal],
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __sub__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]: ...

    @typing.overload
    def __sub__(
        self: Measurement[fractions.Fraction],
        other: Measurement[int] | Measurement[fractions.Fraction],
    ) -> Measurement[fractions.Fraction]: ...

    def __sub__(self, other):
        """Return self - other."""
        return self._apply_operator(other, operator.sub, wrap_in_measurement=True)

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[float],
        other: float,
    ) -> Measurement[float]: ...

    @typing.overload
    def __truediv__(
        self: Measurement[float],
        other: fractions.Fraction,
    ) -> Measurement[float]: ...

    @typing.overload
    def __truediv__(
        self: Measurement[fractions.Fraction],
        other: float,
    ) -> Measurement[float]: ...

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: decimal.Decimal,
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __truediv__(
        self: Measurement[decimal.Decimal],
        other: int | decimal.Decimal,
    ) -> Measurement[decimal.Decimal]: ...

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: fractions.Fraction,
    ) -> Measurement[fractions.Fraction]: ...

    @typing.overload
    def __truediv__(
        self: Measurement[fractions.Fraction],
        other: int | fractions.Fraction,
    ) -> Measurement[fractions.Fraction]: ...

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[float],
        other: Measurement[int] | Measurement[float],
    ) -> float: ...

    @typing.overload
    def __truediv__(
        self: Measurement[float],
        other: Measurement[fractions.Fraction],
    ) -> float: ...

    @typing.overload
    def __truediv__(
        self: Measurement[fractions.Fraction],
        other: Measurement[float],
    ) -> float: ...

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[decimal.Decimal],
        other: Measurement[decimal.Decimal],
    ) -> decimal.Decimal: ...

    @typing.overload
    def __truediv__(
        self: Measurement[decimal.Decimal],
        other: Measurement[int] | Measurement[decimal.Decimal],
    ) -> decimal.Decimal: ...

    @typing.overload
    def __truediv__(
        self: Measurement[int] | Measurement[fractions.Fraction],
        other: Measurement[fractions.Fraction],
    ) -> fractions.Fraction: ...

    @typing.overload
    def __truediv__(
        self: Measurement[fractions.Fraction],
        other: Measurement[int] | Measurement[fractions.Fraction],
    ) -> fractions.Fraction: ...

    def __truediv__(self, other):
        """Return self / other."""
        match other:
            case int() | float() | decimal.Decimal() | fractions.Fraction():
                return self.replace(
                    magnitude=self.magnitude / other,
                )

        return self._apply_operator(other, operator.truediv)

    def __bool__(self: Self) -> bool:
        """Return True if magnitude is nonzero; otherwise return False."""
        return bool(self.magnitude)

    def __int__(self: Self) -> int:
        """Return int(self)."""
        return int(
            (
                self.magnitude
                if self.prefix is MetricPrefix.NONE
                else self.prefix.convert(self.magnitude)
            ),
        )

    def __float__(self: Self) -> float:
        """Return float(self)."""
        return float(
            (
                self.magnitude
                if self.prefix is MetricPrefix.NONE
                else self.prefix.convert(self.magnitude)
            ),
        )

    @typing.overload
    def __round__(
        self: Self,
    ) -> Measurement[int]: ...

    @typing.overload
    def __round__(
        self: Self,
        __ndigits: typing.SupportsIndex,
    ) -> Self: ...

    def __round__(
        self,
        __ndigits=None,
    ):
        """Return round(self)."""
        return self.replace(
            magnitude=round(self.magnitude, __ndigits),
        )


__all__ = [
    "Measurement",
]
