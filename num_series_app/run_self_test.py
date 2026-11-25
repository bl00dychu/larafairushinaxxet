"""Автономные проверки проекта без pytest."""
from __future__ import annotations
import random
import traceback
from num_series import (
    random_series,
    sine_series,
    trend_series,
    mean,
    median,
    spread,
    summarize,
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
)
from num_series.generator import _validate_n
from num_series.deque_average import (
    simple_moving_average_deque
)
_CHECKS = []

def check(name: str):
    """Регистрирует функцию-проверку."""

    def decorator(function):
        _CHECKS.append((name, function))
        return function

    return decorator

def _approx(
    actual,
    expected,
    eps: float = 1e-9
) -> bool:
    """Сравнивает значения с допустимой погрешностью."""

    if isinstance(actual, (list, tuple)):

        return (
            isinstance(expected, (list, tuple))
            and len(actual) == len(expected)
            and all(
                _approx(a, b, eps)
                for a, b in zip(actual, expected)
            )
        )

    return abs(actual - expected) <= eps

def _raises(
    function,
    exception_type=ValueError
) -> bool:
    """Проверяет возникновение исключения."""

    try:
        function()

    except exception_type:
        return True

    except Exception:
        return False

    return False

@check("mean: базовые случаи")
def _check_mean():

    assert _approx(
        mean([1, 2, 3]),
        2.0
    )

    assert _approx(
        mean([1, 2, 3, 4]),
        2.5
    )

@check("mean: пустой ряд -> ValueError")
def _check_mean_empty():

    assert _raises(
        lambda: mean([])
    )

@check("median: чётный/нечётный ряд и выброс")
def _check_median():

    assert median([1, 2, 3]) == 2

    assert _approx(
        median([1, 2, 3, 4]),
        2.5
    )

    assert median(
        [1, 2, 3, 4, 1000]
    ) == 3

@check("spread и summarize")
def _check_summary():

    assert _approx(
        spread([-5, 5]),
        10
    )

    result = summarize(
        [1, 2, 3, 4, 5]
    )

    assert set(result) == {
        "count",
        "mean",
        "median",
        "spread",
        "min",
        "max"
    }

    assert result["count"] == 5

    assert _approx(
        result["mean"],
        3.0
    )

@check("SMA: классика и совпадение с наивной формулой")
def _check_sma():

    assert _approx(
        simple_moving_average(
            [1, 2, 3, 4, 5],
            3
        ),
        [2.0, 3.0, 4.0]
    )

    rng = random.Random(0)

    data = [
        rng.uniform(-10, 10)
        for _ in range(50)
    ]

    window = 7

    naive = [
        sum(data[i:i + window]) / window
        for i in range(len(data) - window + 1)
    ]

    assert _approx(
        simple_moving_average(data, window),
        naive
    )

@check("SMA deque: совпадение с list")
def _check_deque():

    rng = random.Random(42)

    data = [
        rng.uniform(-20, 20)
        for _ in range(60)
    ]

    assert _approx(
        simple_moving_average_deque(data, 5),
        simple_moving_average(data, 5)
    )

@check("SMA/CMA/EMA: обработка некорректных параметров")
def _check_errors():

    assert _raises(
        lambda: simple_moving_average([1, 2, 3], 0)
    )

    assert _raises(
        lambda: simple_moving_average([1, 2], 5)
    )

    assert _raises(
        lambda: centered_moving_average([1, 2, 3, 4], 2)
    )

    assert _raises(
        lambda: exponential_moving_average([1, 2], 0)
    )

    assert _raises(
        lambda: exponential_moving_average([1, 2], 1.5)
    )

@check("генераторы: воспроизводимость и проверка n")
def _check_generators():

    assert (
        random_series(10, seed=42)
        == random_series(10, seed=42)
    )

    assert (
        sine_series(10, noise=1.0, seed=1)
        == sine_series(10, noise=1.0, seed=1)
    )

    assert (
        trend_series(10, noise=0.5, seed=2)
        == trend_series(10, noise=0.5, seed=2)
    )

    for bad_value in (
        -1,
        0,
        3.5,
        "abc",
        None,
        [5]
    ):

        assert _raises(
            lambda value=bad_value: _validate_n(value)
        )

def main() -> int:
    """Запускает все зарегистрированные проверки."""

    passed = 0
    failed = 0

    print(
        f"Запуск {len(_CHECKS)} проверок...\n"
    )

    for name, function in _CHECKS:

        try:
            function()

        except Exception:

            failed += 1

            print(f"FAIL {name}")

            traceback.print_exc()

        else:

            passed += 1

            print(f"OK   {name}")

    total = passed + failed

    print(
        f"\nИтог: {passed}/{total} прошло, "
        f"{failed} упало."
    )

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())

