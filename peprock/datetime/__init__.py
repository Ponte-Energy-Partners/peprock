"""Date/time and related models, helpers and constants.

Complements the datetime package from the standard library
(https://docs.python.org/3/library/datetime.html), adding datetime period models,
timezone awareness helpers and timedelta constants.
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
from .period import (
    Period,
)

__all__ = [
    "ONE_DAY",
    "ONE_HOUR",
    "ONE_MICROSECOND",
    "ONE_MILLISECOND",
    "ONE_MINUTE",
    "ONE_SECOND",
    "ONE_WEEK",
    "EnsureAwareError",
    "Period",
    "__version__",
    "ensure_aware",
    "is_aware",
    "is_naive",
]
