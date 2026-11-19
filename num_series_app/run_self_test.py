"""Минимальная проверка основных функций без установки pytest."""

from num_series import (
    random_series, sine_series, trend_series,
    mean, median, spread, simple_moving_average,
    centered_moving_average, exponential_moving_average,
)


def run_tests():
    assert len(random_series(5, seed=1)) == 5
    assert len(sine_series(8)) == 8
    assert trend_series(3, start=1, step=2) == [1, 3, 5]
    assert mean([1, 2, 3]) == 2
    assert median([1, 2, 3, 4]) == 2.5
    assert spread([1, 5, 3]) == 4
    assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
    assert centered_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
    assert exponential_moving_average([1, 2, 3], 1) == [1.0, 2.0, 3.0]
    print("Все самостоятельные проверки пройдены успешно.")


if __name__ == "__main__":
    run_tests()

