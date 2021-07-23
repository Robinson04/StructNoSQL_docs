### Example :
```python
from StructNoSQL import BaseTable, PrimaryIndex, TableDataModel, BaseField

class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    username = BaseField(name='username', field_type=str, required=False)

class UsersTable(BaseTable):
    def __init__(self):
        super().__init__(table_name='structnosql-example', region_name='eu-west-3', data_model=UsersTableModel, 
                         primary_index=PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str))
        
table = UsersTable()
success = table.put_record({'userId': "testUserId", 'name': 'John'})
```