"""Валидация пользовательского ввода. Проверкатипа данных и допустимых диапазонов. Циклический ввод до получения корректного значения."""

from __future__ import annotations
import math
from connstans import (S_MIN, S_MAX, V_MIN, V_MAX, I_MIN, I_MAX
)
from logger import log_error


def validate_range(value: float, low: float, high: float) -> tuple[bool, str]:
    """Проверка попадания значения в допустим диапазон"""
    if value < low:
        return False, f"Ошибка: значение меньше нижней границы ({low})."
    elif value > high:
        return False, f"Ошибка: значение больше верхней границы ({high})."
    else:
        return True, ""


def input_number(prompt: str, low: float, high: float) -> float:
    """Циклически запрашивать число, пока не будет корректного.Проверяет тип (float) через try/except ValueError и границы."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError as e:
            msg = str(e.args[0]) if e.args else str(e)
            msg = f"Ошибка: введено не число ('{raw}'). {msg}"
            print(msg)
            log_error(msg)
            continue
        #проверка не бесконечно ли число и число ли вовсе
        if not math.isfinite(value):
            msg = f"Ошибка: введите конечное число."
            print(msg)
            log_error(msg)
            continue
        ok, msg = validate_range(value, low, high)
        if ok:
            return value
        print(msg + " Повторите ввод.")
        log_error(msg)

def input_thickness() -> float:
    """Ввод толщины металла s (0.5-20 мм)."""
    return input_number(
        "Введите толщину металла s (0.5-20 мм): ",
        S_MIN,
        S_MAX
    )
def input_speed() -> float:
    """Ввод скорости сварки v (5-80 м/ч)."""
    return input_number(
        "Введите скорость сварки v (5-80 м/ч): ",
        V_MIN,
        V_MAX
    )
def input_current() -> float:
    """Ввод сварочного тока I (20-400 А)."""
    return input_number(
        "Введите сварочный ток I (20-400 А): ",
        I_MIN,
        I_MAX
    )    