"Базовые статистические показатели числового ряда."""
from typing import Dict, Sequence

def _ensure_not_empty(data: Sequence[float]) -> None:
    if len(data) == 0:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")

def mean(data: Sequence[float]) -> float:
    """Среднее арифметическое."""
    _ensure_not_empty(data)
    return sum(data) / len(data)

def median(data: Sequence[float]) -> float:
    """Медиана."""
    _ensure_not_empty(data)
    values = sorted(data)
    middle = len(values) // 2
    if len(values) % 2:
        return float(values[middle])
    return (values[middle - 1] + values[middle]) / 2.0

def spread(data: Sequence[float]) -> float:
    """Размах ряда: максимальное значение минус минимальное."""
    _ensure_not_empty(data)
    return float(max(data) - min(data))

def summarize(data: Sequence[float]) -> Dict[str, float]:
    """Возвращает count, mean, median, spread, min и max."""
    _ensure_not_empty(data)
    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": float(min(data)),
        "max": float(max(data)),
    }

