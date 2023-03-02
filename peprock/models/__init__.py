"""General purpose model classes."""

# noinspection PyProtectedMember
from peprock._version import __version__

from .metric_prefix import MetricPrefix

__all__ = [
    "__version__",
    "MetricPrefix",
]
