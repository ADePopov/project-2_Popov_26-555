from prompt import string
import shlex


def welcome():
    print('Первая попытка запустить проект!')
    print()
    print('')
    print('***')
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    while True:
        command = string('Введите команду: ').strip().lower()

        if command == 'exit':
            break
        elif command == 'help':
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        else:
            print('Неизвестная команда. Введите help для справки')

from primitive_db.engine import (
                                load_metadata, 
                                create_table, 
                                drop_table,
                                save_metadata
)

def run(filepath):
    while True:
        metadata = load_metadata(filepath) 
        print('Формат запроса: create_table 'name_table' 'str' 'int' 'st...'')
        user_input = string('Введите запрос: ').strip().lower()
        lexer = shlex.shlex(user_input)
        col = []
        if lexer[0] == 'create_table':
            if isinstance(lexer[1], str):
                for lex in lexer[2:]:
                    if isinstance(lex, str):
                        col.append(lex)
                    else:
                        print(f'Добавление атрибута - {lex} невозможно, так как это не строка')
                create_table(metadata, lexer[1], col)            
                save_metadata(filepath, lexer)
            else:
                print(f'Название таблицы не принято {lexer[1]} - не является строкой.')
                
        elif lexer[0] == 'drop_table':
        return metadata
