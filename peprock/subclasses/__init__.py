"""Class hierarchy helpers."""

from __future__ import annotations

import inspect
import typing

# noinspection PyProtectedMember
from peprock._version import __version__

if typing.TYPE_CHECKING:
    T_co = typing.TypeVar("T_co", covariant=True)


def get(
    base_class: type[T_co],
    *,
    exclude_abstract: bool = False,
    recursive: bool = False,
) -> set[type[T_co]]:
    """Identify subclasses of base_class and return a set."""
    subclasses: set[type[T_co]] = set()

    for subclass in base_class.__subclasses__():
        if recursive:
            subclasses |= get(
                subclass,
                exclude_abstract=exclude_abstract,
                recursive=recursive,
            )

        if exclude_abstract and inspect.isabstract(subclass):
            continue

        subclasses.add(subclass)

    return subclasses


def get_by_name(
    base_class: type[T_co],
    name: str,
    *,
    recursive: bool = False,
) -> type[T_co] | None:
    """Identify subclass of base_class with given name."""
    for subclass in base_class.__subclasses__():
        if subclass.__name__ == name:
            return subclass

        if recursive and (
            subclass_ := get_by_name(
                base_class=subclass,
                name=name,
                recursive=recursive,
            )
        ):
            return subclass_

    return None


__all__ = [
    "__version__",
    "get",
    "get_by_name",
]
