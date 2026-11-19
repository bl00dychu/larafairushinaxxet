import pytest
from num_series.stats import mean, median, spread, summarize


def test_statistics():
    values = [1, 2, 3, 4, 5]
    assert mean(values) == 3
    assert median(values) == 3
    assert spread(values) == 4
    assert summarize(values)["count"] == 5


def test_even_median():
    assert median([1, 2, 3, 4]) == 2.5


def test_empty():
    with pytest.raises(ValueError):
        mean([])

