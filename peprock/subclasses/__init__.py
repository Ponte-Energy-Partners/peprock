import inspect
import typing

# noinspection PyProtectedMember
from peprock._version import __version__

_T_co = typing.TypeVar("_T_co", covariant=True)


def get(
    base_class: type[_T_co],
    *,
    exclude_abstract: bool = False,
    recursive: bool = False,
) -> set[type[_T_co]]:
    subclasses: set[type[_T_co]] = set()

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
    base_class: type[_T_co],
    name: str,
    *,
    recursive: bool = False,
) -> type[_T_co] | None:
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
