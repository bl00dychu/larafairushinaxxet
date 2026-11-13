import math

print("~~~~~~~~~~~~~~~~~~")
print("Параметры сварки")
print("~~~~~~~~~~~~~~~~~~")

print("=== Параметры сварки ===")
print("1 — Ручная дуговая сварка")
print("2 — MIG/MAG")
print("3 — TIG")

meth = input("Выберите способ сварки (1-3): ")
while (meth != "1") and (meth != "2") and (meth != "3"):
    print("Ошибка: выберите вариант от 1 до 3")
    meth = input("Выберите номер еще раз: ")

if meth == "1":
    k = 1.0 
    U = 25 
    name = "Ручная дуговая сварка"
elif meth == "2": 
    k = 1.15 
    U = 25 
    name = "MIG/MAG" 
elif meth == "3": 
    k = 0.85 
    U = 20 
    name = "TIG" 
else: 
    print("Ошибка: выберите вариант от 1 до 3")


s=0
s2= False
while s2 == False:
    try:
        s = float(input("Введите толщину металла s (0.5-20 мм): "))
        if (s>=0.5) and (s<=20):
            s2 = True
        else:
            print("Ошибка: толщина должна быть от 0.5 до 20 мм")
    except ValueError:
        print("Ошибка: введите число")

v=0
v2= False
while v2 == False:
    try:
        v = float(input("Введите скорость сварки v (5-80 м/ч): "))
        if (v>=5) and (v<=80):
            v2 = True
        else:
            print("Ошибка: скорость должна быть от 5 до 80 м/ч")
    except ValueError:
        print("Ошибка: введите число")   

I=0
I2= False
while I2 == False:
    try:
        I = float(input("Введите сварочный ток I (20-400 А): "))
        if (I>=20) and (I<=400):
            I2 = True
        else:
            print("Ошибка: ток должен быть от 20 до 400 А")
    except ValueError:
        print("Ошибка: введите число")            


d = 0.036 * math.sqrt(I) 
eta = 0.8 
alpha = 10
P = k * I * U * eta / v
V_napl = k * I * alpha / v

if s < 2:
    thickness = "Тонкий металл"
elif s <= 8:
    thickness = "Средний металл"
else:
    thickness = "Толстый металл"

print("~~~~~~~~~~~~~~~~~~")
print("Результаты расчета")
print("~~~~~~~~~~~~~~~~~~")
print("Способ сварки:", name)
print(f"Диаметр электрода: {d:.3f} мм")
print(f"Погонная энергия: {P:.2f}")
print(f"Производительность: {V_napl:.2f}")
print("Класс толщины:", thickness)

print("~~~~~~~~~~~~~~~~~~")
print("Расчет завершен")
print("~~~~~~~~~~~~~~~~~~")