import abc

import pytest

import peprock.subclasses


class _A1:
    pass


class _A2(abc.ABC):
    @abc.abstractmethod
    def method(self) -> None:
        raise NotImplementedError


class _B1(_A1):
    pass


class _B2(_A1, abc.ABC):
    @abc.abstractmethod
    def method(self) -> None:
        raise NotImplementedError


class _B3(_A1, _A2, abc.ABC):
    pass


class _B4(_A1, _A2):
    def method(self) -> None:
        return None


class _B5(_A2, abc.ABC):
    pass


class _B6(_A2):
    def method(self) -> None:
        return None


class _C1(_B1):
    pass


class _C2(_B1, abc.ABC):
    @abc.abstractmethod
    def method(self) -> None:
        raise NotImplementedError


@pytest.mark.parametrize(
    ("base_class", "exclude_abstract", "recursive", "expected"),
    [
        (_A1, False, False, {_B1, _B2, _B3, _B4}),
        (_A1, False, True, {_B1, _B2, _B3, _B4, _C1, _C2}),
        (_A1, True, False, {_B1, _B4}),
        (_A1, True, True, {_B1, _B4, _C1}),
        (_A2, False, False, {_B3, _B4, _B5, _B6}),
        (_A2, False, True, {_B3, _B4, _B5, _B6}),
        (_A2, True, False, {_B4, _B6}),
        (_A2, True, True, {_B4, _B6}),
        (_B1, False, False, {_C1, _C2}),
        (_B1, False, True, {_C1, _C2}),
        (_B1, True, False, {_C1}),
        (_B1, True, True, {_C1}),
        (_B2, False, False, set()),
        (_B2, False, True, set()),
        (_B2, True, False, set()),
        (_B2, True, True, set()),
        (_C1, False, False, set()),
        (_C1, False, True, set()),
        (_C1, True, False, set()),
        (_C1, True, True, set()),
    ],
)
def test_get(base_class, exclude_abstract, recursive, expected):
    assert (
        peprock.subclasses.get(
            base_class,
            exclude_abstract=exclude_abstract,
            recursive=recursive,
        )
        == expected
    )


@pytest.mark.parametrize(
    ("base_class", "name", "recursive", "expected"),
    [
        (_A1, _A1.__name__, False, None),
        (_A1, _A1.__name__, True, None),
        (_A1, _A2.__name__, False, None),
        (_A1, _A2.__name__, True, None),
        (_A1, _B1.__name__, False, _B1),
        (_A1, _B1.__name__, True, _B1),
        (_A1, _B2.__name__, False, _B2),
        (_A1, _B2.__name__, True, _B2),
        (_A1, _B3.__name__, False, _B3),
        (_A1, _B3.__name__, True, _B3),
        (_A1, _B4.__name__, False, _B4),
        (_A1, _B4.__name__, True, _B4),
        (_A1, _B5.__name__, False, None),
        (_A1, _B5.__name__, True, None),
        (_A1, _B6.__name__, False, None),
        (_A1, _B6.__name__, True, None),
        (_A1, _C1.__name__, False, None),
        (_A1, _C1.__name__, True, _C1),
        (_A1, _C2.__name__, False, None),
        (_A1, _C2.__name__, True, _C2),
        (_B1, _A1.__name__, False, None),
        (_B1, _A1.__name__, True, None),
        (_B1, _A2.__name__, False, None),
        (_B1, _A2.__name__, True, None),
        (_B1, _B1.__name__, False, None),
        (_B1, _B1.__name__, True, None),
        (_B1, _B2.__name__, False, None),
        (_B1, _B2.__name__, True, None),
        (_B1, _B3.__name__, False, None),
        (_B1, _B3.__name__, True, None),
        (_B1, _B4.__name__, False, None),
        (_B1, _B4.__name__, True, None),
        (_B1, _B5.__name__, False, None),
        (_B1, _B5.__name__, True, None),
        (_B1, _B6.__name__, False, None),
        (_B1, _B6.__name__, True, None),
        (_B1, _C1.__name__, False, _C1),
        (_B1, _C1.__name__, True, _C1),
        (_B1, _C2.__name__, False, _C2),
        (_B1, _C2.__name__, True, _C2),
    ],
)
def test_get_by_name(base_class, name, recursive, expected):
    assert (
        peprock.subclasses.get_by_name(
            base_class,
            name,
            recursive=recursive,
        )
        == expected
    )
