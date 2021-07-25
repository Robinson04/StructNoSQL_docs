---
id: retrieving_fields
title: Retrieving fields
sidebar_label: Retrieving fields
slug: /basics/retrieving_fields
---

#### If not present, all the required parent field's will be created when updating a nested field

#### Trying to update a field on a non-existing record (key_value) will create the record.


You have multiple operations at your disposition :

- [get_field](../api/get_field.md)
- [get_multiple_fields](../api/get_multiple_fields.md)

todo: should querying fields be included here, or have its own page ?


### Creating the table for our example
```python
import json
from typing import Dict
from StructNoSQL import TableDataModel, BaseField, MapModel, DynamoDBBasicTable, PrimaryIndex

class UsersTableModel(TableDataModel):
    accountId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)
    class FriendItemModel(MapModel):
        name = BaseField(field_type=str, required=True)
        relationship = BaseField(field_type=str, required=False)
        achievements = BaseField(field_type=Dict[str, bool], key_name='achievementKeyName', required=False)
    friends = BaseField(field_type=Dict[str, FriendItemModel], key_name='friendId', required=False)
    class MetadataModel(MapModel):
        lastLoginTimestamp = BaseField(field_type=int, required=False)
    metadata = BaseField(field_type=MetadataModel, required=False)

class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(
            hash_key_name='userId', 
            hash_key_variable_python_type=str
        )
        super().__init__(
            table_name="my-first-table", region_name="eu-west-2", 
            primary_index=primary_index, auto_create_table=True,
            data_model=UsersTableModel
        )

table_client = UsersTable()

with open("record.json", 'r') as file:
    source_record_data: dict = json.load(fp=file)
    put_record_success: bool = table_client.put_record(record_dict_data=source_record_data)
    if put_record_success is not True:
        print("Error with put_record")
```


### 1 - Getting a single field value
Updating a field can only be done by selecting a record with its primary key value through the ```key_value``` parameter 
(primary key values are unique in DynamoDB). 
Specify the field you want to update with the ```field_path```.
And the value to update with ```value_to_set```.
```python
from typing import Optional

retrieved_value: Optional[str] = table_client.get_field(
    key_value='x42', field_path='username'
)
```

### 2 - Getting a single field value without data validation
When retrieving a field, the retrieved data will be passed through the data validation of your table. If the value or
some parts of it are invalid, they will be removed. The data validation is unforced client side by StructNoSQL, not on 
the database side which might cause the retrieved_value to be None or have less items than is actually present in the 
database.

If you need to disable the data_validation and actually retrieve Any data present in the database without any checks or
alterations being done, you can disable it by passing False to dhe ```data_validation``` parameter.

```python
from typing import Optional, Any

retrieved_value: Optional[Any] = table_client.get_field(
    key_value='x42', field_path='username', data_validation=False
)
```
Notice that in our ```get_field``` example, we typed the retrieved_value with ```Optional[str]``` where we assumed that
if the value is not None (with ```Optional```), it will be a ```str```, as per the table model that would only return a 
```str``` as a valid value. Now, since the data_validation is returned, our retrieved value could be anything, so we
type it as ```Optional[Any]```. Note that typing Python code is strictly optional and does not changes anything during
the execution of your code, it is only there to make your code clearer and for your IDE to give quality warnings.

