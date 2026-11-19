from __future__ import annotations
from collections import deque
from typing import Sequence

def _ensure_not_empty(data: Sequence[float]) -> None:
    """Проверяет, что числовой ряд не пустой."""
    if not data:
        raise ValueError(
            "Ряд пуст: расчёт скользящей средней невозможен"
        )
def _check_window(window: int, n: int) -> None:
    """Проверяет корректность размера окна."""
    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError(
            f"window должен быть целым, получено: {window!r}"
        )
    if window <= 0:
        raise ValueError("window должен быть больше нуля")

    if window > n:
        raise ValueError(
            "window не может быть больше длины ряда"
        )
def _check_alpha(alpha: float) -> None:
    """Проверяет коэффициент сглаживания."""
    if not isinstance(alpha, (int, float)) or isinstance(alpha, bool):
        raise ValueError("alpha должен быть числом")

    if not 0 < alpha <= 1:
        raise ValueError("alpha должен находиться в диапазоне (0, 1]")
def simple_moving_average_deque(
    data: Sequence[float],
    window: int
) -> list[float]:
    """Простая скользящая средняя через deque."""
    _ensure_not_empty(data)
    _check_window(window, len(data))

    q = deque(maxlen=window)
    result = []
    current_sum = 0.0

    for value in data:
        if len(q) == window:
            current_sum -= q[0]

        q.append(value)
        current_sum += value

        if len(q) == window:
            result.append(current_sum / window)

    return result

def centered_moving_average_deque(
    data: Sequence[float],
    window: int
) -> list[float]:
    """Центрированная скользящая средняя через deque."""
    _ensure_not_empty(data)
    _check_window(window, len(data))

    if window % 2 == 0:
        raise ValueError("Для центрированной средней окно должно быть нечётным")

    return simple_moving_average_deque(data, window)

def exponential_moving_average_deque(
    data: Sequence[float],
    alpha: float
) -> list[float]:
    """Экспоненциальная скользящая средняя через deque."""
    _ensure_not_empty(data)
    _check_alpha(alpha)

    q = deque(maxlen=1)
    result = []

    for value in data:
        if not q:
            current = float(value)
        else:
            current = alpha * value + (1 - alpha) * q[0]

        q.append(current)
        result.append(current)

    return result