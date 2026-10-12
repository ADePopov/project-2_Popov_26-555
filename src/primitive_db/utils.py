import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath) -> dict:
    """
    load_metadata(filepath): Загружает данные из JSON-файла.
    Если файл не найден, возвращает пустой словарь {}
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_metadata(filepath, data: dict) -> bool:
    """
    save_metadata(filepath, data): Сохраняет переданные данные в JSON-файл.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except OSError as e:
        print(f"Ошибка: {e}")
        return False


def load_table_data(table_name: str) -> list[dict]:
    """
    загружает ранее внесенные данные для таблицы в json формате
    """
    filepath = f"{DATA_DIR}/{table_name}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_table_data(table_name: str, data: list[dict]) -> None:
    """
    сохраняет вносимые данные для таблицы в json формате
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = f"{DATA_DIR}/{table_name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
