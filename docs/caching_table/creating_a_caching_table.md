---
id: creating_a_caching_table
title: Creating a caching table
---

:::info First time using StructNoSQL ?
Consider first creating a ```DynamoDBBasicTable```, and after having understood the basics, migrate to using a 
```DynamoDBCachingTable```. Follow the tutorial at [Creating your first table](../basics/__creating_your_first_table.md)
:::


When creating your table client class, instead of inheriting from BasicTable, simply change it to CachingTable.
All operations work's the with the same functions and parameters for the ```DynamoDBCachingTable``` as for the ```DynamoDBBasicTable```.
Your table model will also not requires any modifications when moving to a ```DynamoDBCachingTable```.

Turn this :
```python
from StructNoSQL import PrimaryIndex, DynamoDBBasicTable

class UsersTable(DynamoDBBasicTable):
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
```

To this :
```python
from StructNoSQL import PrimaryIndex, DynamoDBCachingTable  # <-- Note the change

class UsersTable(DynamoDBCachingTable):  # <-- Note the change
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
```

You know 

