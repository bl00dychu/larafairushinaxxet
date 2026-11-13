from validation import (input_thickness, input_speed, input_current)                        
from menu import show_menu, select_meth
from operations import (electrode_diameter, line_energy, deposition_productivity, thickness_class)    

def main() -> None:
    """Главная функция проги."""
    print("~~~~~~~~~~~~~~~~~~")
    print("Параметры сварки")
    print("~~~~~~~~~~~~~~~~~~")

    while True:
        show_menu()
        meth = select_meth()
        if meth is None:
            print("Работа завершена.")
            break
        k, U, name = meth

        s = input_thickness()
        v = input_speed()
        I = input_current()

        d = electrode_diameter(I)
        P = line_energy(k, I, U, v)
        V_napl = deposition_productivity(k, I, v)
        thickness = thickness_class(s)

        print("\n~~~~~~~~~~~~~~~~~~")
        print("Результаты расчёта")
        print("~~~~~~~~~~~~~~~~~~")
        print("Способ сварки:", name)
        print(f"Диаметр электрода: {d:.3f} мм")
        print(f"Погонная энергия: {P:.2f}")
        print(f"Производительность: {V_napl:.2f}")
        print("Класс толщины:", thickness)
        print("\n~~~~~~~~~~~~~~~~~~")
        print("Расчёт завершён")
        print("~~~~~~~~~~~~~~~~~~")


if __name__ == "__main__":
    main()