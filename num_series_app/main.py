"""CLI приложения для генерации, загрузки и анализа числовых рядов.
Примеры:
  python -m pip install pytest
  python -m pytest
  python main.py --kind sine --n 20 --window 3 --alpha 0.3 --seed 7
  python main.py --kind random --n 1000 --window 10 --benchmark
  python main.py --kind random --n 50 --save data/random.json
  python main.py --load data/random.json --window 5
  python main.py --load data/series.csv --window 5
  python main.py --kind trend --n 30 --export out.csv
"""
from __future__ import annotations
import argparse
import csv
import sys
from typing import List, Optional, Tuple
from num_series import (
    random_series,
    sine_series,
    trend_series,
    summarize,
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
    save_series_json,
    load_series_auto,
    benchmark_moving_average,
)
def build_series(
    kind: str,
    n: int,
    seed: int
) -> List[float]:
    """Генерирует числовой ряд заданного типа."""

    if kind == "random":
        return random_series(
            n,
            low=-50,
            high=50,
            seed=seed
        )

    if kind == "sine":
        return sine_series(
            n,
            amplitude=10,
            frequency=2,
            noise=1.5,
            seed=seed
        )

    if kind == "trend":
        return trend_series(
            n,
            start=0,
            step=1.0,
            noise=0.5,
            seed=seed
        )

    raise ValueError(
        f"Неизвестный тип ряда: {kind!r}"
    )

def obtain_series(
    args: argparse.Namespace
) -> Tuple[List[float], str]:
    """Получает ряд из файла или генератора."""

    if args.load:
        data = load_series_auto(args.load)

        return data, f"файл: {args.load}"

    data = build_series(
        args.kind,
        args.n,
        args.seed
    )

    source = (
        f"сгенерирован ({args.kind}, "
        f"n={args.n}, seed={args.seed})"
    )

    return data, source

def export_series_csv(
    path: str,
    data: List[float],
    sma: Optional[List[float]] = None,
    ema: Optional[List[float]] = None
) -> None:
    """Экспортирует исходный ряд и скользящие средние в CSV."""

    try:
        with open(
            path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if sma is None or ema is None:
                writer.writerow(["i", "value"])

                for i, value in enumerate(data):
                    writer.writerow([i, value])

            else:
                writer.writerow([
                    "i",
                    "value",
                ])

                for i, value in enumerate(data):

                    sma_value = (
                        sma[i]
                        if i < len(sma)
                        else ""
                    )

                    ema_value = (
                        ema[i]
                        if i < len(ema)
                        else ""
                    )

                    writer.writerow([
                        i,
                        value,
                        sma_value,
                        ema_value
                    ])

    except OSError as err:
        raise ValueError(
            f"Не удалось записать CSV {path}: {err}"
        ) from err

def print_series(
    title: str,
    values: List[float],
    fmt: str = "{:>10.3f}"
) -> None:
    """Выводит числовой ряд."""

    print(f"\n{title} (n={len(values)}):")

    print(
        " " + " ".join(
            fmt.format(value)
            for value in values
        )
    )

def print_header(source: str) -> None:
    print("=" * 60)

    print(f"Источник данных: {source}")

    print("-" * 60)

def print_stats(stats: dict) -> None:
    """Выводит статистические показатели."""

    print(
        f"Количество элементов : {stats['count']}"
    )

    print(
        f"Среднее арифметическое : "
        f"{stats['mean']:>10.4f}"
    )

    print(
        f"Медиана : "
        f"{stats['median']:>10.4f}"
    )

    print(
        f"Размах (max - min) : "
        f"{stats['spread']:>10.4f}"
    )

    print(
        f"min / max : "
        f"{stats['min']:>10.4f} / "
        f"{stats['max']:.4f}"
    )
def print_footer() -> None:
    print("=" * 60)

def build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки."""

    parser = argparse.ArgumentParser(
        description="Алгоритмическая обработка числовых рядов",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--kind",
        choices=["random", "sine", "trend"],
        default="sine",
        help="тип генерируемого ряда"
    )

    parser.add_argument(
        "--n",
        type=int,
        default=20,
        help="количество точек в ряде"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="зерно генератора случайных чисел"
    )

    parser.add_argument(
        "--load",
        metavar="PATH",
        help="загрузить ряд из JSON, TXT или CSV"
    )

    parser.add_argument(
        "--save",
        metavar="PATH",
        help="сохранить ряд в JSON"
    )

    parser.add_argument(
        "--export",
        metavar="FILE",
        help="экспортировать данные в CSV"
    )

    parser.add_argument(
        "--window",
        type=int,
        default=3,
        help="размер окна SMA"
    )

    parser.add_argument(
        "--alpha",
        type=float,
        default=0.3,
        help="коэффициент сглаживания EMA"
    )

    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="сравнить скорость list и deque"
    )

    return parser

def main(
    argv: Optional[List[str]] = None
) -> int:
    """Главная функция приложения."""

    args = build_parser().parse_args(argv)
    # Получение данных
    try:
        data, source = obtain_series(args)

    except ValueError as err:
        print(
            f"Ошибка получения ряда: {err}",
            file=sys.stderr
        )

        return 1
    # Сохранение в JSON
    if args.save:

        meta = {
            "source": source
        }

        if not args.load:
            meta.update({
                "kind": args.kind,
                "seed": args.seed
            })

        try:
            save_series_json(
                data,
                args.save,
                meta=meta
            )

            print(
                f"[сохранено] {args.save} "
                f"({len(data)} точек)"
            )

        except ValueError as err:
            print(
                f"Ошибка сохранения: {err}",
                file=sys.stderr
            )

            return 1
    # Расчёт статистики и скользящих средних
    try:
        stats = summarize(data)

        sma = simple_moving_average(
            data,
            args.window
        )

        ema = exponential_moving_average(
            data,
            args.alpha
        )

        cma = (
            centered_moving_average(
                data,
                args.window
            )
            if args.window % 2 == 1
            else None
        )

    except ValueError as err:
        print(
            f"Ошибка анализа: {err}",
            file=sys.stderr
        )

        return 1
    # Экспорт в CSV
    if args.export:

        try:
            export_series_csv(
                args.export,
                data,
                sma,
                ema
            )

            print(
                f"[экспортировано] {args.export}"
            )

        except ValueError as err:
            print(
                f"Ошибка экспорта: {err}",
                file=sys.stderr
            )

            return 1
    # Вывод результатов
    print_header(source)

    print_stats(stats)

    print_series(
        "Исходный ряд",
        data
    )

    print_series(
        f"SMA (window={args.window})",
        sma
    )

    print_series(
        f"EMA (alpha={args.alpha})",
        ema
    )

    if cma is not None:
        print_series(
            f"Центрированное MA (window={args.window})",
            cma
        )
    # Бенчмарк
    if args.benchmark:

        print("\n" + "-" * 60)

        print(
            "Замер времени выполнения SMA "
            "(среднее за 1000 повторов):"
        )

        timings = benchmark_moving_average(
            data,
            args.window,
            repeats=1000
        )

        print(
            f"list  : {timings['list']:.8f} с"
        )

        print(
            f"deque : {timings['deque']:.8f} с"
        )

        if timings["deque"] > 0:
            print(
                "Отношение (list/deque): "
                f"{timings['list'] / timings['deque']:.2f}"
            )
    print_footer()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
