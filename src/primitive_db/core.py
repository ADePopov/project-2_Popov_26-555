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
