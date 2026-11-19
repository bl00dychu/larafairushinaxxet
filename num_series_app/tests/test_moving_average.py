import pytest
from num_series.moving_average import (
    simple_moving_average, centered_moving_average,
    exponential_moving_average,
)


def test_sma_example():
    assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


def test_sma_window_too_large():
    with pytest.raises(ValueError):
        simple_moving_average([1, 2], 3)


def test_centered():
    assert centered_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


def test_ema():
    assert exponential_moving_average([1, 2, 3], 1) == [1.0, 2.0, 3.0]

