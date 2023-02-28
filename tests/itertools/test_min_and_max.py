import pytest

import peprock.itertools


@pytest.mark.parametrize(
    ("iterable", "expected"),
    [
        ((), peprock.itertools.EmptyIterableError),
        ((1,), (1, 1)),
        (range(10), (0, 9)),
        ({0.1, 2.3, 4.5}, (0.1, 4.5)),
        ("word", ("d", "w")),
        ({"a": 9, "b": 2}, ("a", "b")),
    ],
)
def test_max_and_min(iterable, expected):
    match expected:
        case left, right:
            assert peprock.itertools.min_and_max(iterable) == (left, right)
        case _:
            with pytest.raises(expected):
                peprock.itertools.min_and_max(iterable)
