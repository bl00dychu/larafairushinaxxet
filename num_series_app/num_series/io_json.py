"""Сохранение и чтение числовых рядов в формате JSON."""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

PathLike = Union[str, Path]

def save_series_json(
    data: List[float],
    path: PathLike,
    meta: Optional[Dict[str, Any]] = None,
    indent: int = 2,
) -> None:
    """Сохраняет числовой ряд и метаданные в JSON."""
    if not data:
        raise ValueError("Ряд пуст: нечего сохранять")

    for i, value in enumerate(data):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"Элемент data[{i}] = {value!r} не является числом")

    payload = {
        "meta": {
            "n": len(data),
            "created": datetime.now().isoformat(timespec="seconds"),
            **(meta or {}),
        },
        "data": list(data),
    }

    file_path = Path(path)
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=indent)
    except OSError as err:
        raise ValueError(f"Не удалось записать файл {file_path}: {err}") from err

def load_series_json(path: PathLike, with_meta: bool = False):
    """Загружает ряд из JSON; поддерживает список или объект с полем data."""
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except json.JSONDecodeError as err:
        raise ValueError(
            f"Файл {file_path} не является корректным JSON: "
            f"{err.msg} (строка {err.lineno})"
        ) from err
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл {file_path}: {err}") from err

    if isinstance(payload, list):
        data, meta = payload, {}
    elif isinstance(payload, dict):
        if "data" not in payload:
            raise ValueError(f"В файле {file_path} нет поля 'data'")
        data = payload["data"]
        meta = payload.get("meta", {}) or {}
    else:
        raise ValueError(
            f"Некорректная структура JSON в {file_path}: "
            "ожидался список или объект с 'data'"
        )

    if not isinstance(data, list):
        raise ValueError(f"Поле 'data' в {file_path} должно быть списком")
    if not data:
        raise ValueError(f"Ряд в файле {file_path} пуст")

    for i, value in enumerate(data):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(
                f"Элемент data[{i}] = {value!r} в {file_path} не является числом"
            )

    result = [float(value) for value in data]
    return (result, meta) if with_meta else result