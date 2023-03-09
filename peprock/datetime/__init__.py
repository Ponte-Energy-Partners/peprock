"""Date/time and related helpers and constants.

Complements the datetime package from the standard library
(https://docs.python.org/3/library/datetime.html), adding timezone awareness helpers and
timedelta constants.
"""

# noinspection PyProtectedMember
from peprock._version import __version__

from .awareness import EnsureAwareError, ensure_aware, is_aware, is_naive
from .constants import (
    ONE_DAY,
    ONE_HOUR,
    ONE_MICROSECOND,
    ONE_MILLISECOND,
    ONE_MINUTE,
    ONE_SECOND,
    ONE_WEEK,
)

__all__ = [
    "__version__",
    "ONE_MICROSECOND",
    "ONE_MILLISECOND",
    "ONE_SECOND",
    "ONE_MINUTE",
    "ONE_HOUR",
    "ONE_DAY",
    "ONE_WEEK",
    "is_naive",
    "is_aware",
    "EnsureAwareError",
    "ensure_aware",
]
