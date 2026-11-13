import math
# --- коэффиценты способ сварки---
# u-напряжение свароч дуги и k-коэффициент способа сварки

#ручная дуговая
K_ARC: float = 1.0  
U_ARC: float = 25.0 
#сварка в среде защитн газа
K_MIG_MAG: float = 1.15  
U_MIG_MAG: float =25.0
#аргодуговая сварка
K_TIG: float = 0.85 
U_TIG: float = 20.0 

# --- Допустимые диапазоны входных данных ---
S_MIN: float = 0.5
S_MAX: float = 20.0

V_MIN: float = 5.0
V_MAX: float = 80.0

I_MIN: float = 20.0
I_MAX: float = 400.0

# ---Константы для расчёта ---
D_COEFF: float = 0.036
ETA: float = 0.8
ALPHA: float = 10.0

# --- Пороговые значения толщины металла ---
S_THIN_LIMIT: float = 2.0 #толщина меньше 2 - тонкий 
S_MEDIUM_LIMIT: float = 8.0 #толщина от 2 до 8 - средний

# --- Файл журнала ошибок ---
LOG_FILE: str = "input_errors.log"