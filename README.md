# primitive-db

Учебный проект — имитация базы данных на Python. Метаданные хранятся в JSON-файле, команды вводятся через CLI.

## Установка и запуск

```bash
uv sync
uv run python -m primitive_db.main
```

Либо после установки как CLI-инструмента:

```bash
uv tool install .
database
```

> Примечание: демонстрации записаны в Linux (WSL), где проект запускается через `uv run`.

## Управление таблицами

Доступные команды:

- `create_table <имя_таблицы> <столбец1:тип> ...` — создать таблицу
- `drop_table <имя_таблицы>` — удалить таблицу
- `list_tables` — показать все таблицы
- `help` — справка
- `exit` — выход

Типы данных: `int`, `str`, `bool`. Столбец `ID:int` добавляется автоматически.

Пример:

```
Введите запрос: create_table users name str age int
Введите запрос: list_tables
users
Введите запрос: drop_table users
Вы уверены, что хотите выполнить удаление таблицы? [y/n]: y
Введите запрос: exit
```

Демонстрация:

[![asciicast](https://asciinema.org/a/SzmSTccoFuRRusOz.svg)](https://asciinema.org/a/SzmSTccoFuRRusOz)

## CRUD-операции

Программа поддерживает все четыре базовые операции с данными: Create, Read, Update, Delete.

Доступные команды:

- `insert <имя_таблицы> <значение1> <значение2> ...` — добавить запись
- `select <имя_таблицы> [where <столбец> = <значение> ...]` — показать записи
- `update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение>` — обновить записи
- `delete <имя_таблицы> [where <столбец> = <значение> ...]` — удалить записи

Правила ввода:

- Строковые значения — в кавычках: `'Аня'`, `'Боря'`.
- Числа — без кавычек: `25`, `30`.
- Логические — `true` / `false`.
- Условия в `where` объединяются через И (все должны совпасть).
- Столбец `ID` добавляется автоматически — в `insert` его указывать не нужно.

Примеры:

```
insert users Аня 25
insert users Боря 30
insert orders 500 true
```

```
select users
select users where age = 25
select users where name = 'Аня'
select users where age = 25 name = 'Аня'
```

```
update users set age = 26 where name = 'Аня'
update orders set paid = false where price = 500
```

```
delete users where age = 30
delete orders where paid = false
delete users
```

Результат `select` выводится в виде таблицы:

```
+----+-------+-----+
| ID | name  | age |
+----+-------+-----+
| 1  | Аня   | 25  |
| 2  | Боря  | 30  |
| 3  | Вася  | 28  |
+----+-------+-----+
```

Демонстрация:

[![asciicast](https://asciinema.org/a/umPSKlT5GQemkwgt.svg)](https://asciinema.org/a/umPSKlT5GQemkwgt)

## Декораторы

Проект использует декораторы для сквозной логики: обработки ошибок, подтверждения опасных операций, замера времени и кэширования. Они вынесены в отдельный модуль `decorators.py`.

### handle_db_errors — обработка ошибок

Перехватывает `KeyError`, `ValueError`, `FileNotFoundError` и возвращает сообщение вместо падения программы. Применяется к `insert`, `drop_table`, `update`, `delete`.

Пример:

```
insert users Гриша abc
→ Ошибка: некорректный тип данных
```

### confirm_action — подтверждение опасных операций

Спрашивает подтверждение перед выполнением. Применяется к `drop_table` и `delete`.

Пример:

```
delete users
→ Вы уверены, что хотите выполнить удаление данных? [y/n]: n
→ Действие отменено
```

### log_time — замер времени

Печатает, за сколько секунд выполнилась функция. Применяется к `insert` и `select`.

Пример:

```
insert users Аня 25
→ Функция выполнилась за 0.0003 секунд
```

### create_cacher — кэширование select

Повторный одинаковый запрос не читает файл заново — отдаёт результат из кэша. Кэш сбрасывается после `insert`, `update`, `delete`, `drop_table`, `create_table`.

Демонстрация:

[![asciicast](https://asciinema.org/a/CS3B89lEdZYJeFvo.svg)](https://asciinema.org/a/CS3B89lEdZYJeFvo)

## Структура проекта

```
src/primitive_db/
__init__.py
main.py          # точка входа
engine.py        # цикл программы, парсинг команд
сore.py          # CRUD-операции
utils.py         # работа с JSON-файлами
decorators.py    # декораторы
constants.py     # константы
```