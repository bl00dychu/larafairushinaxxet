"""Генерация числовых рядов: случайного, синусоидального и линейного."""
import math
import random
from typing import List, Optional

def _validate_n(n: int) -> None:
    """Проверяет, что n — положительное целое число."""
    try:
        is_positive_int = (n > 0) and (int(n) == n)
    except (TypeError, ValueError, OverflowError) as err:
        raise ValueError(
            f"n должно быть положительным целым числом "
            f"(получено: {n!r}; причина: {err})"
        ) from err

    if isinstance(n, bool) or not is_positive_int:
        raise ValueError(
            f"n должно быть положительным целым числом (получено: {n!r})"
        )

def random_series(
    n: int,
    low: float = -100.0,
    high: float = 100.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Создаёт ряд из n случайных чисел на [low, high]."""
    _validate_n(n)
    if low >= high:
        raise ValueError(f"low должно быть меньше high (получено: {low} >= {high})")
    rng = random.Random(seed)
    return [rng.uniform(low, high) for _ in range(n)]

def sine_series(
    n: int,
    amplitude: float = 1.0,
    frequency: float = 1.0,
    noise: float = 0.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Создаёт синусоидальный ряд с аддитивным шумом."""
    _validate_n(n)
    if noise < 0:
        raise ValueError("noise не может быть отрицательным")
    rng = random.Random(seed)
    return [
        amplitude * math.sin(2 * math.pi * frequency * i / n)
        + (rng.uniform(-noise, noise) if noise else 0.0)
        for i in range(n)
    ]

def trend_series(
    n: int,
    start: float = 0.0,
    step: float = 1.0,
    noise: float = 0.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Создаёт линейный тренд с необязательным шумом."""
    _validate_n(n)
    if noise < 0:
        raise ValueError("noise не может быть отрицательным")
    rng = random.Random(seed)
    return [
        start + step * i + (rng.uniform(-noise, noise) if noise else 0.0)
        for i in range(n)
    ]

