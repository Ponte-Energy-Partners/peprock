## 1.7.8 (2024-12-22)

## 1.7.7 (2024-12-22)

## 1.7.6 (2024-12-08)

## 1.7.5 (2024-12-08)

## 1.7.4 (2024-12-08)

### Fix

- **patterns**: apply PEP 570 to `Observer.notify()`
- **models**: apply PEP 570 to `Measurement.__round__()`

## 1.7.3 (2024-10-28)

## 1.7.2 (2024-10-27)

## 1.7.1 (2024-10-15)

### Refactor

- simplify version sourcing
- apply ruff preview recommendations

## 1.7.0 (2023-12-25)

### Feat

- **datetime**: implement `peprock.datetime.Period`

## 1.6.3 (2023-11-03)

### Refactor

- improve type hint

### Perf

- **models**: optimize `Unit.symbol`
- **models**: optimize `Measurement.__format__()`

## 1.6.2 (2023-08-06)

## 1.6.1 (2023-08-06)

## 1.6.0 (2023-03-15)

### Perf

- **models**: optimize `Measurement`

## 1.5.0 (2023-03-12)

### Feat

- **models**: implement `Measurement.replace` and optimize code

## 1.4.0 (2023-03-10)

### Feat

- **models**: support `Measurement.__int__()` and `Measurement.__float__()`

### Refactor

- **models**: provide default for `to` argument in `MetricPrefix.convert()`
- **models**: improve type hints

## 1.3.0 (2023-03-09)

### Refactor

- **models**: optimize return type of private `measurement._normalize_magnitudes()`

## 1.2.1 (2023-03-09)

## 1.2.0 (2023-03-09)

### Feat

- **models**: implement `Measurement` model
- **models**: implement `Unit` model

### Refactor

- use absolute imports only
- **models**: rename position-only arguments and provide fastpath in `MetricPrefix.convert()`

## 1.1.0 (2023-03-03)

### Feat

- **patterns**: implement observer pattern

## 1.0.2 (2023-03-03)

## 1.0.1 (2023-03-03)

## 1.0.0 (2023-03-02)

### Feat

- **itertools**: implement `min_and_max()`
- **typing**: implement `typing` package
- **models**: improve type handling in `MetricPrefix.to()` and `MetricPrefix.convert()`

### Fix

- **models**: add `__all__` to `metrix_prefix.py`

### Refactor

- **typing**: retire `typing`
- **itertools**: retire `itertools`
- **models**: simplify type annotations
- **subclasses**: leverage `peprock.typing.T_co`
- **models**: extract base into constant

### Perf

- **models**: remove cache from `MetricPrefix.to()`

## 0.4.1 (2023-02-26)

### Fix

- **models**: add missing py.typed marker

## 0.4.0 (2023-02-26)

### Feat

- **models**: implement `peprock.models.MetricPrefix`

## 0.3.0 (2023-02-26)

### Refactor

- turn peprock into namespace package

## 0.2.0 (2023-02-25)

### Feat

- **datetime**: implement constants `peprock.datetime.ONE_MICROSECOND`, `peprock.datetime.ONE_MILLISECOND`, `peprock.datetime.ONE_SECOND`, `peprock.datetime.ONE_MINUTE`, `peprock.datetime.ONE_HOUR`, `peprock.datetime.ONE_DAY`, `peprock.datetime.ONE_WEEK`
- **datetime**: implement `peprock.datetime.ensure_aware()`
- **datetime**: implement `peprock.datetime.is_naive()` and `peprock.datetime.is_aware()`

## 0.1.1 (2023-02-24)

## 0.1.0 (2023-02-24)

### Feat

- **subclasses**: implement `peprock.subclasses.get()` and `peprock.subclasses.get_by_name()`
