"""Сохранение и чтение числовых рядов в формате JSON."""
from __future__ import annotations
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

PathLike = Union[str, Path]

def _validate_data(data: List[float]) -> None:
    """Проверяет данные перед сохранением."""

    if not data:
        raise ValueError(
            "Ряд пуст: нечего сохранять или анализировать"
        )

    for index, value in enumerate(data):

        if isinstance(value, bool) or not isinstance(
            value, (int, float)
        ):
            raise ValueError(
                f"Элемент data[{index}] = {value!r} "
                "не является числом"
            )

        if not math.isfinite(float(value)):
            raise ValueError(
                f"Элемент data[{index}] = {value!r} "
                "не является конечным числом"
            )

def save_series_json(
    data: List[float],
    path: PathLike,
    meta: Optional[Dict[str, Any]] = None,
    indent: Optional[int] = 2,
) -> None:
    """Сохраняет числовой ряд в JSON."""

    _validate_data(data)

    if meta is not None and not isinstance(meta, dict):
        raise ValueError(
            "meta должен быть словарём или None"
        )

    file_path = Path(path)

    payload = {
        "meta": {
            **(meta or {}),
            "n": len(data),
            "created": datetime.now().isoformat(
                timespec="seconds"
            ),
        },
        "data": [float(value) for value in data],
    }

    try:
        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(
                payload,
                file,
                ensure_ascii=False,
                indent=indent,
                allow_nan=False
            )

    except (OSError, TypeError, ValueError) as err:
        raise ValueError(
            f"Не удалось записать файл {file_path}: {err}"
        ) from err
    
def load_series_json(
    path: PathLike,
    with_meta: bool = False
):
    """Загружает числовой ряд из JSON."""

    file_path = Path(path)

    if not file_path.exists():
        raise ValueError(
            f"Файл не найден: {file_path}"
        )

    try:
        with file_path.open("r", encoding="utf-8") as file:
            payload = json.load(file)

    except json.JSONDecodeError as err:
        raise ValueError(
            f"Файл {file_path} не является корректным JSON: "
            f"{err.msg} (строка {err.lineno})"
        ) from err

    except OSError as err:
        raise ValueError(
            f"Не удалось прочитать файл {file_path}: {err}"
        ) from err

    if isinstance(payload, list):
        data = payload
        meta = {}

    elif isinstance(payload, dict):

        if "data" not in payload:
            raise ValueError(
                f"В файле {file_path} нет поля 'data'"
            )

        data = payload["data"]
        meta = payload.get("meta", {}) or {}

        if not isinstance(meta, dict):
            raise ValueError(
                f"Поле 'meta' в {file_path} должно быть объектом"
            )

    else:
        raise ValueError(
            "Некорректная структура JSON: "
            "ожидался список или объект с 'data'"
        )

    if not isinstance(data, list):
        raise ValueError(
            f"Поле 'data' в {file_path} должно быть списком"
        )

    if not data:
        raise ValueError(
            f"Ряд в файле {file_path} пуст"
        )

    for index, value in enumerate(data):

        if isinstance(value, bool) or not isinstance(
            value, (int, float)
        ):
            raise ValueError(
                f"Элемент data[{index}] = {value!r} "
                "не является числом"
            )

        if not math.isfinite(float(value)):
            raise ValueError(
                f"Элемент data[{index}] = {value!r} "
                "не является конечным числом"
            )

    result = [float(value) for value in data]

    return (result, meta) if with_meta else result

__all__ = [
    "save_series_json",
    "load_series_json",
]