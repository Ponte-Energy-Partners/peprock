"""Date/time and related models, helpers and constants.

Complements the datetime package from the standard library
(https://docs.python.org/3/library/datetime.html), adding datetime period models
and timezone awareness helpers.
"""

import importlib.metadata

from .awareness import EnsureAwareError, ensure_aware, is_aware, is_naive
from .period import (
    Period,
)

__version__ = importlib.metadata.version("peprock")

__all__ = [
    "EnsureAwareError",
    "Period",
    "__version__",
    "ensure_aware",
    "is_aware",
    "is_naive",
]
