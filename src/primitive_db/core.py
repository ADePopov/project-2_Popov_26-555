from primitive_db.utils import load_table_data


def create_table(
        metadata: dict[str, dict], 
        table_name: str, 
        columns: list[tuple[str, str]]
        ) -> dict[str, dict]:
    '''
    функция create_table(metadata, table_name, columns).
    Принимает текущие метаданные, имя таблицы и список столбцов.
    Автоматически добавляет столбец ID:int в начало списка столбцов.
    Проверяет, не существует ли уже таблица с таким именем. Если да, выводит ошибку.
    Проверяет корректность типов данных (только int, str, bool).
    В случае успеха, обновляет словарь metadata и возвращать его.
    '''
    if table_name in metadata:
        print(f'Ошибка, таблица {table_name} существует.')
        return metadata
    
    allow_data = {'int', 'str', 'bool'}
    for name, col_type in columns:
        if col_type not in allow_data:
            print(f"Ошибка: недопустимый тип {col_type} для столбца {name}.")
            return metadata
        
    full_columns = [{'name':'ID','type':'int'}] + [
        {'name':name, 'type':col_type} for name, col_type in columns
    ]

    metadata[table_name] = {'columns':full_columns}
    return metadata

def drop_table(metadata: dict[str, dict], table_name: str) -> dict[str, dict]:
    '''
    функция drop_table(metadata, table_name).
    Проверяет существование таблицы. Если таблицы нет, выводит ошибку.
    Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    '''
    if table_name not in metadata:
        print(f'Ошибка, таблица {table_name} не существует.') 
        return metadata
    del metadata[table_name]
    return metadata

def list_tables(metadata: dict[str, dict]) -> list[str]:
    """
    Функция list_tables представляет данные о имеющихся таблицах
    в базе данных
    """
    result = list(metadata.keys())
    return result

def insert(metadata: dict[str, dict],
    table_name: str,
    values: list[str],
) -> list[dict] | str:
    """
    Проверяет, существует ли таблица.
    Проверяет, что количество переданных значений соответствует количеству столбцов (минус ID).
    Валидирует типы данных для каждого значения в соответствии со схемой в metadata.
    Генерирует новый ID (например, max(IDs) + 1 или len(data) + 1).
    Добавляет новую запись (в виде словаря) в данные таблицы и возвращает их.
    """
    if table_name not in metadata:
        return f'Таблицы {table_name} - не существует'

    col = [c['type'] for c in metadata[table_name]['columns'] if c['name'] != 'ID']
    col_names = [c["name"] for c in metadata[table_name]["columns"] if c["name"] != "ID"]

    if len(values) != len(col):
        return f'Необходимо {len(col)} значений, получено {len(values)} значений'

    result = []
    for c, v in zip(col, values):
        try:
            if c == 'int':
                result.append(int(v))
            elif c == 'bool':
                low = v.lower()
                if low in ('1', 'true', 'yes'):
                    result.append(True)
                elif low in ('0', 'false', 'no'):
                    result.append(False)
                else:
                    return f"'{v}' не является bool"
            else:
                result.append(str(v))
        except ValueError:
            return f'{v} не соответствует типу {c}'

    data = load_table_data(table_name)

    try:
        new_id = max((row.get("ID", 0) for row in data), default=0) + 1
    except ValueError:
        new_id = 1

    new_row = {"ID": new_id}
    for name, val in zip(col_names, result):
        new_row[name] = val

    data.append(new_row)
    return data

def select(table_data: list[dict], where_clause: dict | None = None) -> list[dict]:
    """
    Возвращает список строк из table_data, соответствующих where_clause.

    Если where_clause is None — возвращает все строки.
    where_clause — словарь {столбец: значение}. Все условия объединяются через И
    """
    if where_clause is None:
        return table_data

    result = []
    for row in table_data:
        if all(row.get(col) == val for col, val in where_clause.items()):
            result.append(row)
    return result

def update(table_data: list[dict], set_clause: dict, where_clause: dict) -> list[dict]:
    """
    func update находит записи по where_clause.
    Обновляет в найденных записях поля согласно set_clause.
    Возвращает измененные данные.
    """
    if not where_clause:
        return table_data

    for row in table_data:
        if all(row.get(col) == val for col, val in where_clause.items()):
            for col, val in set_clause.items():
                row[col] = val
    return table_data

def delete(table_data: list[dict], where_clause: dict | None = None) -> list[dict]:
    """
    Находит записи по where_clause и удаляет их.
    Возвращает измененные данные.
    """
    if where_clause is None:
        return []
    
    result = []
    for row in table_data:
        if all(row.get(col) != val for col, val in where_clause.items()):
            result.append(row)
            
    return result

def pars_where(args:list) -> dict | str:
    """
    Функция парсит введенный список и возвращает словарь
    """
    if len(args) % 3 != 0:
        return f'Некорректный ввод значений'

    result = {}
    for i in range(0, len(args), 3):
        if args[i+1] != '=':
            return f"Присваивание необходимо провести через знак '=', сейчас {args[i+1]}"
        col = args[i]
        raw = args[i + 2]
        if len(raw) >= 2 and raw[0] in ("'", '"') and raw[-1] == raw[0]:
            value = raw[1:-1]
        else:
            if raw.lower() in ("true", "false"):
                value = raw.lower() == "true"
            else:
                try:
                    value = int(raw)
                except ValueError:
                    return f"'{raw}' не является числом"  
        result[col] = value
    return result

def pars_set(args:list) -> dict | str:
    """
    Функция парсит введенный список и возвращает словарь
    """
    if len(args) % 3 != 0:
        return f'Некорректный ввод значений'
    result = {}
    for i in range(0, len(args), 3):
        if args[i+1] != '=':
            return f"Присваивание необходимо провести через знак '=', сейчас {args[i+1]}"
        col = args[i]
        raw = args[i + 2]
        if len(raw) >= 2 and raw[0] in ("'", '"') and raw[-1] == raw[0]:
            value = raw[1:-1]
        else:
            if raw.lower() in ("true", "false"):
                value = raw.lower() == "true"
            else:
                try:
                    value = int(raw)
                except ValueError:
                    return f"'{raw}' не является числом"  
        result[col] = value
    return result

