"""Class hierarchy helpers.

Examples
--------
>>> sorted(get(int), key=lambda t: t.__name__)  # doctest: +SKIP
[<enum 'IntEnum'>, <enum 'IntFlag'>, <class 'sre_constants._NamedIntConstant'>, <class 'bool'>]

>>> get_by_name(int, name="bool")
<class 'bool'>

>>> len(get(object))  # doctest: +SKIP
280


"""  # noqa: E501

from __future__ import annotations

import importlib.metadata
import inspect
import typing

if typing.TYPE_CHECKING:
    T_co = typing.TypeVar("T_co", covariant=True)

__version__ = importlib.metadata.version("peprock")


def _collect_recursive(baseclasses: list[type[T_co]]) -> None:
    for baseclass in baseclasses.copy():
        if subclasses := baseclass.__subclasses__():
            _collect_recursive(subclasses)
            baseclasses.extend(subclasses)


def get(
    base_class: type[T_co],
    *,
    recursive: bool = False,
    exclude_abstract: bool = False,
) -> set[type[T_co]]:
    """Identify subclasses of base_class and return a set."""
    subclasses = base_class.__subclasses__()

    if recursive:
        _collect_recursive(subclasses)

    if exclude_abstract:
        return {subclass for subclass in subclasses if not inspect.isabstract(subclass)}

    return set(subclasses)


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
