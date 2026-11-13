"""Расчёты параметров сварки"""
from typing import Annotated
from connstans import ( D_COEFF, ETA, ALPHA, S_THIN_LIMIT, S_MEDIUM_LIMIT
)

def electrode_diameter(
    current: Annotated[float,  "Сварочный ток, А"],
) -> float:
    """Рассчитать диаметр электрода:d = 0.036 * sqrt(I)"""
    return D_COEFF * current ** 0.5

def line_energy(
    k: Annotated[float, "Коэффициент способа сварки"],
    current: Annotated[float, "Сварочный ток, А"],
    voltage: Annotated[float, "Напряжение, В"],
    speed: Annotated[float, "Скорость сварки, м/ч"],
) -> float:
    """Рассчитать погонную энергию: P = k * I * U * eta / v"""
    return k * current * voltage * ETA / speed

def deposition_productivity(
    k: Annotated[float, "Коэффициент способа сварки"],
    current: Annotated[float, "Сварочный ток, А"],
    speed: Annotated[float, "Скорость сварки, м/ч"],
) -> float:
    """Рассчитать производительность наплавки:V_napl = k * I * alpha / v"""
    return k * current * ALPHA / speed

def thickness_class(
    s: Annotated[float, "Толщина металла, мм"],
) -> str:
    """Классифицировать толщину металла.
    s < 2 — тонкий металл;
    2 <= s <= 8 — средний металл;
    s > 8 — толстый металл.
    """
    if s < S_THIN_LIMIT:
        return "Тонкий металл"
    elif s <= S_MEDIUM_LIMIT:
        return "Средний металл"
    else:
        return "Толстый металл"