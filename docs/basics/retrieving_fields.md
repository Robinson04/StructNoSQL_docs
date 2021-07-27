---
id: retrieving_fields
title: Retrieving fields
sidebar_label: Retrieving fields
slug: /basics/retrieving_fields
---

The 'get' operations can retrieve fields from a record when you select it with its primary key value. To retrieve 
records based on secondary indexes, you need to query your records as showed in the 
[Querying fields](../basics/querying_fields.md) page.

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
You can use [get_field](../api/get_field.md) to retrieve a single field value.
Specify the primary key value of the record you want to retrieve the field from with the ```key_value``` parameter.
Specify the field you want to retrieve with ```field_path```.
```python
from typing import Optional

retrieved_value: Optional[str] = table_client.get_field(
    key_value='x42', field_path='username'
)
```
If no value has been found or if it did not pass the data validation, ```retrieved_value``` will be None.
The typing with ```Optional[str]``` is not required.


### 2 - Getting a single field value without data validation
The retrieved data will be passed through the data validation of your table. If the value or
some parts of it are invalid, they will be removed. The data validation is unforced client side by StructNoSQL, not on 
the database side which might cause the retrieved_value to be None or have less items than is actually present in the 
database.

If you need to disable the data_validation and actually retrieve any data present in the database without any checks or
alterations being done, you can disable it by passing False to the ```data_validation``` parameter.
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


### 3 - Getting multiple fields values with a multi-selector
If you need to retrieve multiple fields that share the same parent path, you can use a multi-selector.
Wrap the multiple fields names you want to retrieve inside parenthesis. This will be similar to using the 
[get_multiple_fields](../api/get_multiple_fields) operation, where the multiple fields will be retrieved with a
single database operation. 
You will be returned a dictionary where the keys will be all the fields names you requested, and their matching 
retrieved values if they were found.
```python
from typing import Dict, Optional, Any

retrieved_values: Dict[str, Optional[Any]] = table_client.get_field(
    key_value='x42', field_path='(username, friends)'
)
retrieved_username_value: Optional[str] = retrieved_values['username']
retrieved_friends_value: Optional[dict] = retrieved_values['friends']
```
No matter what, ```retrieved_values``` will always be a dictionary containing as keys all the names of the 
fields you tried to retrieve. 
Even if the operation failed, the dictionary will be returned with a ```None``` value for each 
field.
You can safely access the fields values with brackets instead of using the ```.get``` function on your dictionary.



### 4 - Getting a single nested field value
```python
from typing import Optional

retrieved_friend_name: Optional[str] = table_client.get_field(
    key_value='x42', field_path='friends.{{friendId}}.name',
    query_kwargs={'friendId': 'f42'}
)
```

### 5 - Getting multiple nested fields values with a multi-selector
You can use multi-selectors even with nested fields, and even with query_kwargs.
The only constraint, is the multi-selector must be the last 'path element' of your field path.
```python
from typing import Dict, Optional, Any

retrieved_values: Dict[str, Optional[Any]] = table_client.get_field(
    key_value='x42', field_path='friends.{{friendId}}.(name, relationship)',
    query_kwargs={'friendId': 'f42'}
)
retrieved_friend_name_value: Optional[str] = retrieved_values['name']
retrieved_friend_relationship_value: Optional[str] = retrieved_values['relationship']
```
If you need to retrieve fields from totally different places, use [get_multiple_fields](../api/get_multiple_fields)
showcased in the examples below.


### 5 - Getting multiple fields values with get_multiple_fields
You can use [get_multiple_fields](../api/get_multiple_fields) to retrieve multiple fields at once from the same 
record with a single database operation.
Like update_field, you select the record you want to update with its primary key value passed in the ```key_value``` 
parameter.
Specify the different fields you want to retrieved by passing a dictionary of [FieldGetter](../api/FieldGetter).
Similarly to get_field, each [FieldGetter](../api/FieldGetter) requires the field_path parameter, and has an optional 
query_kwargs parameter.
```python
from typing import Dict, Optional, Any
from StructNoSQL import FieldGetter

retrieved_values: Dict[str, Optional[Any]] = table_client.get_multiple_fields(
    key_value='x42', getters={
        'username': FieldGetter(field_path='username'),
        'friend_relationship': FieldGetter(
            field_path='friends.{{friendId}}.relationship', 
            query_kwargs={'friendId': 'f42'}, 
        ),
        'metadata_lastLoginTimestamp': FieldGetter(
            field_path='metadata.lastLoginTimestamp', 
        )
    }
)
retrieved_username: Optional[str] = retrieved_values['username']
retrieved_friend_relationship: Optional[str] = retrieved_values['friend_relationship']
retrieved_last_login_timestamp: Optional[int] = retrieved_values['metadata_lastLoginTimestamp']
```
No matter what, ```retrieved_values``` will always be a dictionary containing as keys all the names of the 
fields you tried to retrieve. 
Even if the operation failed, the dictionary will be returned with a ```None``` value for each 
field.
You can safely access the fields values with brackets instead of using the ```.get``` function on your dictionary.



### 6 - Getting multiple fields values with get_multiple_fields without data validation
The retrieved data will be passed through the data validation of your table. If the value or
some parts of it are invalid, they will be removed. The data validation is unforced client side by StructNoSQL, not on 
the database side which might cause the retrieved_value to be None or have less items than is actually present in the 
database.

If you need to disable the data_validation and actually retrieve any data present in the database without any checks or
alterations being done, you can disable it by passing False to the ```data_validation``` parameter.
```python
from typing import Dict, Optional, Any
from StructNoSQL import FieldGetter

retrieved_values: Dict[str, Optional[Any]] = table_client.get_multiple_fields(
    key_value='x42', getters={
        'username': FieldGetter(field_path='username'),
        'friend_relationship': FieldGetter(
            field_path='friends.{{friendId}}.relationship', 
            query_kwargs={'friendId': 'f42'}, 
        ),
        'metadata_lastLoginTimestamp': FieldGetter(
            field_path='metadata.lastLoginTimestamp', 
        )
    }, data_validation=False  # <-- disable data_validation
)
retrieved_username: Optional[Any] = retrieved_values['username']
retrieved_friend_relationship: Optional[Any] = retrieved_values['friend_relationship']
retrieved_last_login_timestamp: Optional[Any] = retrieved_values['metadata_lastLoginTimestamp']
```