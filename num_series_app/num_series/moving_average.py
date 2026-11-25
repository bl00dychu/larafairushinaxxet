"""
Алгоритмы скользящего среднего:
SMA, центрированное MA и EMA.
"""
from __future__ import annotations
import math
import time
from collections import deque
from typing import Dict, List, Sequence

def _ensure_not_empty(data: Sequence[float]) -> None:
    if data is None or len(data) == 0:
        raise ValueError(
            "Ряд пуст: расчёт скользящей средней невозможен"
        )
def check_window(window: int, n: int) -> None:
    """Проверяет размер окна."""

    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError(
            f"window должен быть целым, получено: {window!r}"
        )

    if window < 1:
        raise ValueError(
            f"window должен быть >= 1, получено: {window}"
        )

    if window > n:
        raise ValueError(
            f"window ({window}) больше длины ряда ({n}) — "
            "скользящее среднее невозможно"
        )
def _check_alpha(alpha: float) -> float:
    """Проверяет коэффициент сглаживания EMA."""

    if isinstance(alpha, bool):
        raise ValueError(
            f"alpha должен быть в (0, 1], получено: {alpha!r}"
        )

    try:
        value = float(alpha)
    except (TypeError, ValueError, OverflowError) as err:
        raise ValueError(
            f"alpha должен быть в (0, 1], получено: {alpha!r}"
        ) from err

    if not math.isfinite(value) or not (0.0 < value <= 1.0):
        raise ValueError(
            f"alpha должен быть в (0, 1], получено: {alpha!r}"
        )

    return value

def simple_moving_average(
    data: Sequence[float],
    window: int
) -> List[float]:
    """Простая скользящая средняя через бегущую сумму O(n)."""

    _ensure_not_empty(data)
    check_window(window, len(data))

    running_sum = float(sum(data[:window]))
    result = [running_sum / window]

    for index in range(window, len(data)):
        running_sum += data[index] - data[index - window]
        result.append(running_sum / window)

    return result

def centered_moving_average(
    data: Sequence[float],
    window: int
) -> List[float]:
    """Центрированная скользящая средняя."""

    _ensure_not_empty(data)
    check_window(window, len(data))

    if window % 2 == 0:
        raise ValueError(
            "Центрированное MA требует нечётного окна; "
            f"window должно быть нечётным, получено: {window}"
        )

    return simple_moving_average(data, window)

def exponential_moving_average(
    data: Sequence[float],
    alpha: float
) -> List[float]:
    """Экспоненциальная скользящая средняя."""

    _ensure_not_empty(data)
    alpha_value = _check_alpha(alpha)

    previous = float(data[0])
    result = [previous]

    for value in data[1:]:
        previous = (
            alpha_value * value
            + (1.0 - alpha_value) * previous
        )
        result.append(float(previous))

    return result

def simple_moving_average_deque(
    data: Sequence[float],
    window: int
) -> List[float]:
    """SMA с использованием collections.deque."""

    _ensure_not_empty(data)
    check_window(window, len(data))

    buffer = deque(maxlen=window)
    running_sum = 0.0
    result = []

    for value in data:

        if len(buffer) == window:
            running_sum -= buffer[0]

        buffer.append(value)
        running_sum += value

        if len(buffer) == window:
            result.append(running_sum / window)

    return result

def benchmark_moving_average(
    data: Sequence[float],
    window: int,
    repeats: int = 1000
) -> Dict[str, float]:
    """Сравнивает скорость list- и deque-реализаций SMA."""

    _ensure_not_empty(data)
    check_window(window, len(data))

    if (
        not isinstance(repeats, int)
        or isinstance(repeats, bool)
        or repeats < 1
    ):
        raise ValueError(
            f"repeats должен быть положительным целым, "
            f"получено: {repeats!r}"
        )

    started = time.perf_counter()

    for _ in range(repeats):
        simple_moving_average(data, window)

    list_time = (
        time.perf_counter() - started
    ) / repeats

    started = time.perf_counter()

    for _ in range(repeats):
        simple_moving_average_deque(data, window)

    deque_time = (
        time.perf_counter() - started
    ) / repeats

    return {
        "list": list_time,
        "deque": deque_time
    }

__all__ = [
    "check_window",
    "simple_moving_average",
    "centered_moving_average",
    "exponential_moving_average",
    "simple_moving_average_deque",
    "benchmark_moving_average",
]
