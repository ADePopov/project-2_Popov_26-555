metadata = {
    "users": {
        "columns": [
            {"name": "ID", "type": "int"},
            {"name": "name", "type": "str"},
            {"name": "age", "type": "int"}
        ]
    },
    "orders": {
        "columns": [
            {"name": "ID", "type": "int"},
            {"name": "price", "type": "int"},
            {"name": "paid", "type": "bool"}
        ]
    }
}

data = [
    {"ID": 1, "name": "Аня", "age": 25},
    {"ID": 2, "name": "Боря", "age": 30},
    {"ID": 3, "name": "Вася", "age": 28}
]
data_empty = [
    {"ID": 1, "name": "Аня", "age": 25}
]




s = ['age', '=', '28']



if len(s) % 3 != 0:
    print(f'некорректный ввод значений')
t = len(s) // 3

count = 0
dicts = {}
for i in range(t):
    s[count:count+3]
    dicts[s[count:count+3][0]] = s[count:count+3][2]
    count += 3
print(dicts)
metadata['users']



  
