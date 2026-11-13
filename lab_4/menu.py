""" Меню выбора режима обработки через match-case. """
from __future__ import annotations
from connstans import (K_ARC, U_ARC, K_MIG_MAG, U_MIG_MAG, K_TIG, U_TIG                      
)
from logger import log_error

def show_menu() -> None:
    """Вывести меню способа сварки."""
    print("\n=== Выберите способ сварки ===")
    print("1 — Ручная дуговая сварка")
    print("2 — MIG/MAG")
    print("3 — TIG")
    print("0 — Выход")

def select_meth() -> tuple[float, float, str]  | None:
    #тапл,тк функц возвращает 3 знач
    """Запрашивать способ сварки до корректного ввода. Возвращает коэффициент k, напряжение U и название способа.
    None — выход из программы."""
    while True:
        choice = input("Выберите способ сварки (0-3):").strip()
        match choice:
            case "1":
                return K_ARC, U_ARC, "Ручная дуговая сварка"
            case "2":
                return K_MIG_MAG, U_MIG_MAG, "MIG/MAG"
            case "3":
                return K_TIG, U_TIG, "TIG"
            case "0":
                return None
            case _:
                msg = "Ошибка: выберите вариант от 0 до 3."
                print(msg)
                log_error(msg)


#не делалаб тк через тапл все объединила 
# def mode_name(k: float) -> str:
#     """Вернуть название режима по коэффициенту k."""
#     match k:
#         case 1.0:
#             return "черновая"
#         case 0.85:
#             return "получистовая"
#         case 0.7:
#             return "чистовая"
#         case _:
#             return "неизвестный"