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

def insert(metadata, table_name, values):
    """
    Проверяет, существует ли таблица.
    Проверяет, что количество переданных значений соответствует количеству столбцов (минус ID).
    Валидирует типы данных для каждого значения в соответствии со схемой в metadata.
    Генерирует новый ID (например, max(IDs) + 1 или len(data) + 1).
    Добавляет новую запись (в виде словаря) в данные таблицы и возвращает их.
    """
    if table_name not in metadata:
        return f'Таблицы {table_name} - не существует'

    val_col = len(metadata[table_name]['columns'])
    val = len(values)
    if val_col - 1 < val:
        return f'количество передаваемых значений не соответствует количеству столбцов. {val_col} < {val}'

    col = [col['type'] for col in metadata[table_name]['columns']]
    for val, c in zip(values, col):
        if not type(val).__name__==c:
            return f'Тип введенное значение не соответсвует необходимому значению. {type(val).__name__} != {c}'