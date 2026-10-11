import shlex
from prompt import string
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    drop_table,
    list_tables,
    insert,
    select,
    update,
    delete,
    pars_where,
    pars_set
)
from primitive_db.utils import  (
    load_metadata,
    save_metadata,
    load_table_data,
    save_table_data
)

def print_table(rows: list[dict]) -> None:
    """Печатает список словарей как таблицу."""
    if not rows:
        print("Ничего не найдено")
        return

    table = PrettyTable()
    table.field_names = list(rows[0].keys())  

    for row in rows:
        table.add_row([row.get(col, "") for col in table.field_names])

    print(table)

def welcome():
    print('Первая попытка запустить проект!')
    print()
    print('***')
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")


def run(filepath):
    '''
    Основная функция отвечающая за вызовы:
    create_table
    drop_table
    list_tables
    '''
    while True:
        metadata = load_metadata(filepath)
        
        user_input = string('Введите запрос: ').strip()
        if not user_input:
            continue

        lexer = shlex.split(user_input, posix=False)
        if not lexer:
            continue
        com = lexer[0].lower()

        if com == 'exit':
            break

        elif com == 'help':
            print("\n***Процесс работы с таблицей***")
            print("Функции:")
            print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
            print("<command> list_tables - показать список всех таблиц")
            print("<command> drop_table <имя_таблицы> - удалить таблицу")
            print("<command> insert <имя_таблицы> <значение1> <значение2> ... - добавить запись")
            print("<command> select <имя_таблицы> [where <столбец> = <значение> ...] - показать записи")
            print("<command> update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение> - обновить записи")
            print("<command> delete <имя_таблицы> [where <столбец> = <значение> ...] - удалить записи")
            print()
            print("\nОбщие команды:")
            print("<command> exit - выход из программы")
            print("<command> help - справочная информация\n")
            
        elif com == 'create_table':
            if len(lexer) < 4:
                print(f'Ошибка: нужно имя таблицы и хотя бы один столбец, какой будет тип. Сейчас {len(lexer)}') 
                continue
            table_name = lexer[1]
            atr = lexer[2:]
            if len(atr) % 2 != 0:
                print('Ошибка: имя столбца и атрибуты должны быть парными')
                continue
            col = [(atr[i], atr[i+1]) for i in range(0, len(atr), 2)]
            metadata = create_table(metadata, table_name, col)
            save_metadata(filepath, metadata)

        elif com == 'drop_table':
            if len(lexer) < 2:
                print('Ошибка: указаны не все атрибуты. Необходимо указать название таблицы')
                continue
            metadata = drop_table(metadata, lexer[1])
            save_metadata(filepath, metadata)

        elif com == 'list_tables':
            res = list_tables(metadata)
            if not res:
                print('Таблиц нет')
            else:
                for r in res:
                    print(r) 

        elif com == 'insert':
            if len(lexer) < 3:
                print("Ошибка: нужно имя таблицы и хотя бы одно значение")
                continue

            table_name = lexer[1]
            values = lexer[2:]

            if table_name not in metadata:
                print(f"Таблица '{table_name}' не существует")
                continue

            result = insert(metadata, table_name, values)

            if isinstance(result, str):
                print(result)
                continue

            save_table_data(table_name, result)
            print("Запись добавлена")

        elif com == 'select':
            if len(lexer) < 2:
                print("Ошибка: укажи имя таблицы")
                continue

            table_name = lexer[1]

            if table_name not in metadata:
                print(f"Таблица '{table_name}' не существует")
                continue

            if 'where' in lexer:
                i = lexer.index('where')
                where_part = lexer[i + 1:]
                where_clause = pars_where(where_part)

                if isinstance(where_clause, str):
                    print(where_clause)
                    continue
            else:
                where_clause = None

            table_data = load_table_data(table_name)
            result = select(table_data, where_clause)

            print_table(result)
        
        elif com == 'update':
            if 'set' not in lexer or 'where' not in lexer:
                print("Ошибка: нужны части 'set' и 'where'")
                continue

            table_name = lexer[1]

            if table_name not in metadata:
                print(f"Таблица '{table_name}' не существует")
                continue

            i_set = lexer.index('set')
            i_where = lexer.index('where')

            set_part = lexer[i_set + 1:i_where]
            where_part = lexer[i_where + 1:]

            set_clause = pars_set(set_part)
            where_clause = pars_where(where_part)

            if isinstance(set_clause, str):
                print(set_clause)
                continue
            if isinstance(where_clause, str):
                print(where_clause)
                continue

            table_data = load_table_data(table_name)
            result = update(table_data, set_clause, where_clause)
            save_table_data(table_name, result)
            print("Данные обновлены")

        elif com == 'delete':
            if len(lexer) < 2:
                print("Ошибка: укажи имя таблицы")
                continue

            table_name = lexer[1]

            if table_name not in metadata:
                print(f"Таблица '{table_name}' не существует")
                continue

            if 'where' in lexer:
                i = lexer.index('where')
                where_part = lexer[i + 1:]
                where_clause = pars_where(where_part)

                if isinstance(where_clause, str):
                    print(where_clause)
                    continue
            else:
                where_clause = None

            table_data = load_table_data(table_name)
            result = delete(table_data, where_clause)
            save_table_data(table_name, result)
            print("Данные удалены")

        else:
            print('Неизвестная команда')
