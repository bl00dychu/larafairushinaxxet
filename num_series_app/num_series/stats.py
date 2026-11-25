"""
Модуль расчёта статистических показателей.
Реализованы:
- среднее арифметическое;
- медиана;
- размах;
- сводная статистика.
"""
from typing import Dict, Sequence

def _ensure_not_empty(data: Sequence[float]) -> None:
    """Проверяет, что числовой ряд не пуст."""

    if len(data) == 0:
        raise ValueError(
            "Ряд пуст: расчёт статистики невозможен"
        )

def mean(data: Sequence[float]) -> float:
    """Вычисляет среднее арифметическое."""

    _ensure_not_empty(data)

    return sum(data) / len(data)

def median(data: Sequence[float]) -> float:
    """Вычисляет медиану."""

    _ensure_not_empty(data)

    s = sorted(data)
    k = len(s) // 2

    if len(s) % 2:
        return float(s[k])

    return (s[k - 1] + s[k]) / 2.0

def spread(data: Sequence[float]) -> float:
    """Вычисляет размах ряда: max - min."""

    _ensure_not_empty(data)

    return float(max(data) - min(data))

def summarize(data: Sequence[float]) -> Dict[str, float]:
    """Формирует сводный отчёт по числовому ряду."""

    _ensure_not_empty(data)

    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": float(min(data)),
        "max": float(max(data)),
    }