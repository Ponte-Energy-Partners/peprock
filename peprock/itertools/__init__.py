# noinspection PyProtectedMember
from peprock._version import __version__

from .min_and_max import EmptyIterableError, min_and_max

__all__ = [
    "__version__",
    "EmptyIterableError",
    "min_and_max",
]
