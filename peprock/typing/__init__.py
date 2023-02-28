from __future__ import annotations

import typing

# noinspection PyProtectedMember
from peprock._version import __version__

T = typing.TypeVar("T")
T_co = typing.TypeVar("T_co", covariant=True)
T_contra = typing.TypeVar("T_contra", contravariant=True)


class SupportsLessThan(typing.Protocol[T_contra]):
    def __lt__(self: SupportsLessThan, other: T_contra) -> bool:
        ...


SupportsLessThanT = typing.TypeVar("SupportsLessThanT", bound=SupportsLessThan)


__all__ = [
    "__version__",
    "T",
    "T_co",
    "T_contra",
    "SupportsLessThan",
    "SupportsLessThanT",
]
