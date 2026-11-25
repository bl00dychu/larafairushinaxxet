"""Скользящие средние на основе collections.deque."""
from __future__ import annotations
import math
from collections import deque
from typing import Deque, List, Sequence

def _ensure_not_empty(data: Sequence[float]) -> None:
    if data is None or len(data) == 0:
        raise ValueError(
            "Ряд пуст: расчёт скользящей средней невозможен"
        )
def _check_window(window: int, n: int) -> None:
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
            f"window ({window}) больше длины ряда ({n}) — SMA невозможна"
        )

def _check_alpha(alpha: float) -> float:
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

    if not math.isfinite(value) or not 0.0 < value <= 1.0:
        raise ValueError(
            f"alpha должен быть в (0, 1], получено: {alpha!r}"
        )

    return value

def simple_moving_average_deque(
    data: Sequence[float],
    window: int
) -> List[float]:
    """SMA через deque."""

    _ensure_not_empty(data)
    _check_window(window, len(data))

    buffer: Deque[float] = deque(maxlen=window)

    running_sum = 0.0
    result = []

    for index, value in enumerate(data):

        if len(buffer) == window:
            running_sum -= buffer[0]

        buffer.append(value)
        running_sum += value

        if index >= window - 1:
            result.append(running_sum / window)

    return result

def centered_moving_average_deque(
    data: Sequence[float],
    window: int
) -> List[float]:
    """Центрированная SMA через deque."""

    _ensure_not_empty(data)
    _check_window(window, len(data))

    if window % 2 == 0:
        raise ValueError(
            "Центрированное MA требует нечётного окна; "
            "window должно быть нечётным"
        )

    return simple_moving_average_deque(data, window)


def exponential_moving_average_deque(
    data: Sequence[float],
    alpha: float
) -> List[float]:
    """EMA с использованием deque для хранения последнего значения."""

    _ensure_not_empty(data)
    alpha_value = _check_alpha(alpha)

    history: Deque[float] = deque(maxlen=1)

    previous = float(data[0])
    result = [previous]

    history.append(previous)

    for value in data[1:]:

        previous = (
            alpha_value * value
            + (1.0 - alpha_value) * previous
        )

        history.append(float(previous))
        result.append(float(previous))

    return result

__all__ = [
    "simple_moving_average_deque",
    "centered_moving_average_deque",
    "exponential_moving_average_deque",
]
