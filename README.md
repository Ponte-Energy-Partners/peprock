# peprock
Foundational Python library

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://docs.python.org/3.10/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![codecov](https://codecov.io/gh/Ponte-Energy-Partners/peprock/branch/main/graph/badge.svg?token=LWI96U2WSI)](https://codecov.io/gh/Ponte-Energy-Partners/peprock)
[![test](https://github.com/Ponte-Energy-Partners/peprock/actions/workflows/test.yml/badge.svg)](https://github.com/Ponte-Energy-Partners/peprock/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/peprock.svg)](https://badge.fury.io/py/peprock)

**peprock** is a collection of versatile Python libraries, provided as namespace packages:

-   **[peprock.datetime](#datetime)**: Date/time and related helpers and constants.
-   **[peprock.models](#models)**: General purpose model classes.
-   **[peprock.subclasses](#subclasses)**: Class hierarchy helpers.

* * *

<h2 id="datetime">peprock.datetime</h2>

Date/time and related helpers and constants.

Complements the [datetime package][] from the standard library, adding timezone awareness helpers and
timedelta constants.

  [datetime package]: https://docs.python.org/3/library/datetime.html

### Timezone awareness helpers

    >>> from datetime import datetime, timezone
    >>> from peprock.datetime import ensure_aware, is_aware, is_naive
    >>> naive = datetime.now()

    >>> is_naive(naive)
    True
    >>> is_aware(naive)
    False

    >>> aware = ensure_aware(naive, assumed_tz=timezone.utc)
    >>> is_naive(aware)
    False
    >>> is_aware(aware)
    True

### Timedelta constants

    >>> from datetime import datetime
    >>> from peprock.datetime import ONE_SECOND, ONE_HOUR

    >>> dt = datetime(2023, 3, 2, 21, 17, 12)
    >>> dt + ONE_HOUR + 5 * ONE_SECOND
    datetime.datetime(2023, 3, 2, 22, 17, 17)

<h2 id="models">peprock.models</h2>

General purpose model classes.

### Metric prefix

    >>> from peprock.models import MetricPrefix

    >>> MetricPrefix.mega.convert(5, to=MetricPrefix.kilo)
    5000
    >>> MetricPrefix.centi.convert(0.7, to=MetricPrefix.milli)
    7.0

<h2 id="subclasses">peprock.subclasses</h2>

Class hierarchy helpers.

    >>> from peprock import subclasses

    >>> subclasses.get(int)
    {<enum 'IntEnum'>, <class 'sre_constants._NamedIntConstant'>, <enum 'IntFlag'>, <class 'bool'>}

    >>> subclasses.get_by_name(int, name="bool")
    <class 'bool'>

    >>> len(subclasses.get(object))
    568
