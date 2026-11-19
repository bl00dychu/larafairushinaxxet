# Лабараторная 5

## Алгоритмическая обработка числовых рядов

Модульное консольное приложение на Python для генерации числовых рядов,
расчёта базовых статистических показателей, вычисления скользящих средних и работы с файлами.

## Структура проекта

```text
num_series_app/
├── num_series/
│   ├── __init__.py
│   ├── generator.py
│   ├── stats.py
│   ├── moving_average.py
│   ├── io_json.py
│   └── io_file.py
├── tests/
│   ├── __init__.py
│   ├── test_generator.py
│   ├── test_stats.py
│   ├── test_moving_average.py
│   └── test_cli.py
├── conftest.py
├── pytest.ini
├── run_self_tests.py
├── main.py
└── README.md
```

main.py-основной файл программы
num_series/generator.py-генерация числовых рядов
num_series/stats.py-статические расчеты
num_series/moving_average.py-скользящие средние
num_series/deque_average.py-реализация скользящих средних с использованием deque
tests/test_generator.py-проверяет правильность числовых рядовЖ случайныйб синусоидальный
tests/test_stats.py-правильность расчета средней арифм,медиан и размерах
tests/test_moving_average.py-правильность расчета скользящих сред SMA,CMA,EMA
tests/test_cli.py-правильность запуска программы через команд стр

## Запуск

Откройте терминал в папке `num_series_app` и выполните:

```bash
python main.py
```

## Примеры из задания

Генерация синусоидального ряда и анализ:

```bash
python main.py --kind sine --n 20 --window 3 --alpha 0.3 --seed 7
```

Генерация случайного ряда и сохранение в JSON:

```bash
python main.py --kind random --n 50 --save data/random.json
```

Загрузка JSON и анализ:

```bash
python main.py --load data/random.json --window 5
```

Загрузка CSV:

```bash
python main.py --load data/series.csv --window 5
```

Генерация тренда и экспорт в CSV:

```bash
python main.py --kind trend --n 30 --export out.csv
```

Вывод результата в JSON:

```bash
python main.py --kind sine --n 20 --json
```

## Параметры

- `--kind`: тип генерируемого ряда `random`, `sine` или `trend`.
- `--n`: количество точек в ряде.
- `--seed`: начальное значение генератора случайных чисел(зерно).
- `--load`: загрузить ряд из JSON, TXT или CSV.
- `--save`: сохранить исходный ряд в JSON.
- `--export`: экспортировать исходный ряд в CSV.
- `--window`: размер окна SMA (для скользящей средней).
- `--alpha`: коэффициент сглаживания для EMA, `0 < alpha <= 1`.
- `--json`: вывести результаты анализа в JSON.

## Проверка

Без дополнительных библиотек:

```bash
python run_self_tests.py
```

Если установлен pytest:

```bash
python -m pytest -v
```

Для работы приложения сторонние библиотеки не нужны.
