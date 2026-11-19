import pytest
from num_series.generator import random_series, sine_series, trend_series

def test_random_reproducible():
    assert random_series(5, seed=7) == random_series(5, seed=7)

def test_sine_length():
    assert len(sine_series(10)) == 10

def test_trend_without_noise():
    assert trend_series(4, start=2, step=3) == [2, 5, 8, 11]

def test_invalid_n():
    with pytest.raises(ValueError):
        random_series(0)