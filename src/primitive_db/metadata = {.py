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
values = '1 sss 222'
values = values.split(' ')
print(values)
table_name = 'users'

col = [col['type'] for col in metadata[table_name]['columns']]
print(col)

result = []
for c, v in zip(col, values):
    if c == 'int':
        result.append(int(v))
    elif c == bool:
        low = v.lower()
        if low in ('1', 'True', 'yes'):
            result.append(True)
        elif low in ('0', 'False', 'no'):
            result.append(False)
        else:
            raise ValueError
    else:
        result.append(str(v))



#emp = set()
#for val, c in zip(values, col):
#    if not type(val).__name__==c:
        #break


