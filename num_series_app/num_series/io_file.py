"""Чтение числовых рядов из TXT и CSV."""
import re
from pathlib import Path
from typing import List, Union
from .io_json import load_series_json

PathLike = Union[str, Path]
_SEPARATORS = re.compile(r"[,;\s]+")

def load_series_txt(path: PathLike) -> List[float]:
    """Читает TXT: по одному числу на строку; пропускает пустые строки и #."""
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    result = []
    try:
        with file_path.open("r", encoding="utf-8") as file:
            for line_number, raw in enumerate(file, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    result.append(float(line))
                except ValueError as err:
                    raise ValueError(
                        f"{file_path}:{line_number}: '{line}' не является числом"
                    ) from err
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл {file_path}: {err}") from err

    if not result:
        raise ValueError(f"Файл {file_path} не содержит чисел")
    return result


def load_series_csv(path: PathLike) -> List[float]:
    """Читает числа через запятую, точку с запятой, пробел или табуляцию."""
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    result = []
    try:
        with file_path.open("r", encoding="utf-8") as file:
            for line_number, raw in enumerate(file, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                tokens = [token for token in _SEPARATORS.split(line) if token]
                if not tokens:
                    continue
                try:
                    values = [float(token) for token in tokens]
                except ValueError as err:
                    if line_number == 1:
                        continue
                    raise ValueError(
                        f"{file_path}:{line_number}: строка '{line}' "
                        "содержит нечисловые значения"
                    ) from err
                result.extend(values)
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл {file_path}: {err}") from err

    if not result:
        raise ValueError(f"Файл {file_path} не содержит чисел")
    return result

def load_series_auto(path: PathLike) -> List[float]:
    """Выбирает загрузчик по расширению файла."""
    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        return load_series_json(path)
    if suffix in {".txt", ".dat"}:
        return load_series_txt(path)
    if suffix in {".csv", ".tsv"}:
        return load_series_csv(path)
    try:
        return load_series_csv(path)
    except ValueError:
        return load_series_txt(path)
