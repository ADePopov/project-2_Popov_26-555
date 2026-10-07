from prompt import string


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
	