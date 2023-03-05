import pytest

import peprock.models


@pytest.mark.parametrize(
    "unit",
    list(peprock.models.Unit),
)
def test_symbol(unit):
    assert isinstance(unit.symbol, str)
    assert unit.symbol == unit.value
    assert peprock.models.Unit(unit.symbol) is unit
