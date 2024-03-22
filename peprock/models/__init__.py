"""General purpose model classes."""

import importlib.metadata

from .measurement import Measurement
from .metric_prefix import MetricPrefix
from .unit import Unit

__version__ = importlib.metadata.version("peprock")

__all__ = [
    "Measurement",
    "MetricPrefix",
    "Unit",
    "__version__",
]
