---
id: creating_your_first_table
title: Creating your first table
sidebar_label: put_record
slug: /api/put_record
---

### Creating a table is done in 2 steps :


#### 1 - Create the model of your table
```python
from StructNoSQL import BaseTable, PrimaryIndex, TableDataModel, BaseField

class UsersTableModel(TableDataModel):
    accountId = BaseField(name='userId', field_type=str, required=True)
    username = BaseField(name='username', field_type=str, required=False)

class UsersTable(BaseTable):
    def __init__(self):
        primary_index = PrimaryIndex(
            hash_key_name='userId', 
            hash_key_variable_python_type=str
        )
        super().__init__(
            table_name="my-first-table", region_name="eu-west-2", 
            primary_index=primary_index, auto_create_table=True,
            data_model=UsersTableModel()
        )

table_client = UsersTable()
```