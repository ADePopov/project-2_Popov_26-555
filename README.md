primitive-db
Учебный проект — имитация базы данных на Python. Метаданные хранятся в JSON-файле, команды вводятся через CLI.

Запуск

uv run python -m primitive_db.main

Управление таблицами.
Команда	с описанием:
create_table - cоздать таблицу
drop_table - удалить таблицу
help - справка
exit - Выход
Типы данных: int, str, bool. 
Столбец ID:int добавляется автоматически.

Пример.
Введите запрос: create_table users name str age int
Введите запрос: drop_table users
Введите запрос: exit