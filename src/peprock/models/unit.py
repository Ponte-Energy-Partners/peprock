"""Unit of measurement model.

See https://en.wikipedia.org/wiki/Unit_of_measurement

Examples
--------
>>> Unit.ohm.symbol
'Ω'

>>> Unit("W")
<Unit.watt: 'W'>


"""

from __future__ import annotations

import enum
import functools


class Unit(enum.Enum):
    """Unit Enum with symbol."""

    # metric units, see https://en.wikipedia.org/wiki/List_of_metric_units
    one = "1"  # unit of a quantity of dimension one
    second = "s"  # unit of time
    metre = "m"  # unit of length
    gram = "g"  # unit of mass (actually kilogram in SI)
    ampere = "A"  # unit of electric current
    kelvin = "K"  # unit of thermodynamic temperature
    mole = "mol"  # unit of amount of substance
    candela = "cd"  # unit of luminous intensity
    hertz = "Hz"  # equal to one reciprocal second
    radian = "rad"  # equal to one
    steradian = "sr"  # equal to one
    newton = "N"  # equal to one kilogram-metre per second squared
    pascal = "Pa"  # equal to one newton per square metre
    joule = "J"  # equal to one newton-metre
    watt = "W"  # equal to one joule per second
    coulomb = "C"  # equal to one ampere second
    volt = "V"  # equal to one joule per coulomb
    weber = "Wb"  # equal to one volt-second
    tesla = "T"  # equal to one weber per square metre
    farad = "F"  # equal to one coulomb per volt
    ohm = "Ω"  # equal to one volt per ampere
    siemens = "S"  # equal to one ampere per volt
    henry = "H"  # equal to one volt-second per ampere
    # degree Celsius (°C) is equal to one kelvin
    lumen = "lm"  # equal to one candela-steradian
    lux = "lx"  # equal to one lumen per square metre
    becquerel = "Bq"  # equal to one reciprocal second
    gray = "Gy"  # equal to one joule per kilogram
    sievert = "Sv"  # equal to one joule per kilogram
    katal = "kat"  # equal to one mole per second

    @functools.cached_property
    def symbol(self: Unit) -> str:
        """Get the unit symbol."""
        return self.value


__all__ = [
    "Unit",
]
