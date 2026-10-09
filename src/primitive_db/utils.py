import json

def load_metadata(filepath) -> dict:
    """
    load_metadata(filepath): Загружает данные из JSON-файла. 
    Если файл не найден, возвращает пустой словарь {}
    """
    try: 
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)  
        return data
    except FileNotFoundError as e:
        return {}
    
def save_metadata(filepath, data: dict) -> bool:
    '''
    save_metadata(filepath, data): Сохраняет переданные данные в JSON-файл.
    '''
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True 
    except OSError as e:
        print(f'Ошибка: {e}')
        return False