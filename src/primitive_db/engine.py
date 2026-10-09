import shlex
from prompt import string

from primitive_db.core import (
    create_table,
    drop_table,
    list_tables
)
from primitive_db.utils import  (
    load_metadata,
    save_metadata
)

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

        lexer = shlex.split(user_input)
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

        else:
            print('Неизвестная команда')
