"""Алгоритмы скользящего среднего."""
from typing import List, Sequence

def check_window(window: int, n: int) -> None:
    """Проверяет размер окна: целое число от 1 до n."""
    if isinstance(window, bool) or not isinstance(window, int) or window < 1:
        raise ValueError("window должно быть целым числом >= 1")
    if window > n:
        raise ValueError(
            f"Размер окна ({window}) не может быть больше длины ряда ({n})"
        )

def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """SMA через бегущую сумму за O(n). Длина результата: n - window + 1."""
    check_window(window, len(data))
    running = sum(data[:window])
    result = [running / window]

    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)

    return result

def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированное скользящее среднее; окно должно быть нечётным. Каждое значение результата относится к центру соответствующего окна.
    Поэтому длина результата равна len(data) - window + 1."""
    if isinstance(window, bool) or not isinstance(window, int) or window % 2 == 0:
        raise ValueError("Для центрированной MA размер окна должен быть нечётным")
    return simple_moving_average(data, window)

def exponential_moving_average(
    data: Sequence[float], alpha: float
) -> List[float]:
    """EMA: EMA[0] = data[0], далее alpha*x[i] + (1-alpha)*EMA[i-1]."""
    if len(data) == 0:
        raise ValueError("Ряд пуст: EMA невозможна")
    if not isinstance(alpha, (int, float)) or isinstance(alpha, bool) or not (0 < alpha <= 1):
        raise ValueError("alpha должен находиться в диапазоне 0 < alpha <= 1")

    result = [float(data[0])]
    for value in data[1:]:
        result.append(alpha * value + (1 - alpha) * result[-1])
    return result