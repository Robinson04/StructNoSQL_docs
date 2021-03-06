---
id: removing_deleting_fields
slug: /basics/removing_deleting_fields
title: Removing & deleting fields
---

The following operations can be performed only by selecting records with their primary key values.
If you need to delete/remove fields by selecting records from secondary indexes or if you need to apply filter
expressions to the record's to alter, do a query operation only retrieving the primary key values of each record as 
showcased in [Querying field](../basics/querying_fields), and then perform the appropriate delete/remove operation's 
for each record.  

For deletion and removal, you have multiple operations at your disposition :

- [delete_field](../api/delete_field.md)
- [delete_multiple_fields](../api/delete_multiple_fields.md)
- [remove_field](../api/remove_field.md)
- [remove_multiple_fields](../api/remove_multiple_fields.md)

:::info You cannot delete or remove the primary key value of a record
{{file::docs_parts/creating_deleting_records/remove_alter_and_create_record_to_change_primary_key_value.md::}}
Refer yourself to [Creating & deleting records (changing a record primary key value by removing and recreating it)](
../basics/creating_deleting_records#4---changing-a-record-primary-key-value-by-removing-and-recreating-it)
{{file::docs_parts/creating_deleting_records/limitation_record_recreation_to_change_primary_key_value.md::}}
::: 

### Creating the table for our example
```python
import json
from typing import Dict
from StructNoSQL import TableDataModel, BaseField, MapModel, \
    DynamoDBBasicTable, PrimaryIndex

class UsersTableModel(TableDataModel):
    accountId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)
    status = BaseField(field_type=str, required=False)
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


### 1 - Deleting a single field value
You can use [delete_field](../api/query_field) to delete a single field value from one record selected by its primary 
key value.
Specify the primary key value of the record you want to delete the field from with the ```key_value``` parameter.
Specify the field you want to delete with ```field_path```.
```python
deletion_success: bool = table_client.delete_field(
    key_value='x42', field_path='friends'
)
```
If the field did not exist, ```deletion_success``` will be ```False```. Otherwise, if the operation succeeded, it will 
be ```True```.


### 2 - Deleting multiple fields values with a multi-selector
If you need to delete multiple fields that share the same parent path, you can use a multi-selector.
Wrap the multiple fields names you want to retrieve inside parenthesis. This will be similar to using the 
[delete_multiple_fields](../api/delete_multiple_fields) operation, where the deletion success of each fields will be 
returned individually.

single database operation. You will be returned a dictionary with the keys will be all the fields names you requested,
and their retrieved values if they were found.
```python
from typing import Dict

deletion_successes: Dict[str, bool] = table_client.delete_field(
    key_value='x42', field_path='(friends, metadata)'
)
friends_deletion_success: bool = deletion_successes['friends']
metadata_deletion_success: bool = deletion_successes['metadata']
```
If you need to delete fields from totally different places, use [delete_multiple_fields](../api/delete_multiple_fields)
showcased in the examples below.

### 3 - Deleting multiple fields values with delete_multiple_fields
{{template::{
    'filepath': 'docs_parts/templates/grouped_fields_operation_template.md', 
    'operation_link': "[delete_multiple_fields](../api/delete_multiple_fields)",
    'type_operation_single': "delete_field", 'alteration_type': "delete",
    'object_link': "[FieldRemover](../api/FieldRemover.md)", 'additional': ""
}::}}
```python
from typing import Dict
from StructNoSQL import FieldRemover

deletion_successes: Dict[str, bool] = table_client.delete_multiple_fields(
    key_value='x42', removers={
        'status': FieldRemover(field_path='status'),
        'friend_relationship': FieldRemover(
            field_path='friends.{{friendId}}.relationship', 
            query_kwargs={'friendId': 'f42'}, 
        ),
        'metadata_lastLoginTimestamp': FieldRemover(
            field_path='metadata.lastLoginTimestamp', 
        )
    }
)
status_deletion_success: bool = deletion_successes['status']
friend_relationship_deletion_success: bool = deletion_successes['friend_relationship']
last_login_timestamp_deletion_success: bool = deletion_successes['metadata_lastLoginTimestamp']
```
{{template::{
    'filepath': 'docs_parts/templates/multi_selectors_template.md',
    'variable_name': "deletion_successes", 'individual_target_type_name': "remover",
    'default_value': "False", 'attempted_operation_explanation': "tried to delete"
}::}}


### 4 - Removing a single field value
You can use [remove_field](../api/remove_field) to remove a single field value from a record (removing : deleting and 
retrieving the removed value in a single database operation).
Similarly to [delete_field](../api/delete_field), you select the record you want to remove the field from with its 
primary key value by passing using the ```key_value``` parameter. And you specify to field to remove with the 
```field_path``` parameter.
```python
from typing import Optional

removed_friends_value: Optional[dict] = table_client.remove_field(
    key_value='x42', field_path='friends'
)
```
You receive as result the removed value. If no field value was found or if the operation failed, a value of None will 
be returned.
Note that receiving a None value does not necessarily mean the operation failed, since you could have allowed the 
```None``` value as one of the accepted values of the field you are trying to remove. 


### 5 - Removing a single field value without data validation
{{file::docs_parts/reason_for_disabling_data_validation.md::}}
```python
from typing import Optional, Any

removed_friends_value: Optional[Any] = table_client.remove_field(
    key_value='x42', field_path='friends', data_validation=False
)
```

### 6 - Removing multiple fields values with a multi-selector
If you need to remove multiple fields that share the same parent path, you can use a multi-selector.
```python
from typing import Dict, Optional, Any

removed_values: Dict[str, Optional[Any]] = table_client.remove_field(
    key_value='x42', field_path='(username, friends)'
)
removed_username_value: Optional[str] = removed_values['username']
removed_friends_value: Optional[dict] = removed_values['friends']
```
{{template::{
    'filepath': 'docs_parts/templates/multi_selectors_template.md', 
    'variable_name': "removed_values", 'individual_target_type_name': "field",
    'default_value': "None", 'attempted_operation_explanation': "tried to remove"
}::}}


### 7 - Removing a nested field value
{{file::docs_parts/targeting_nested_field.md::}}
{{template::{
    'filepath': 'docs_parts/alter_nested_item_template.md', 'alteration': "remove"
}::}} 
```python
from typing import Optional

removed_friend_relationship: Optional[str] = table_client.remove_field(
    key_value='x42', field_path='friends.{{friendId}}.relationship',
    query_kwargs={'friendId': 'f42'}
)
```

### 8 - Removing multiple nested fields values with a multi-selector
You can also use a multi-selector in a nested ```field_path```, in which case the keys in ```removed_values``` will be
the name's of each field in your multi-selector (not their entire field_path's).
```python
from typing import Dict, Optional, Any

removed_values: Dict[str, Optional[Any]] = table_client.remove_field(
    key_value='x42', field_path='friends.{{friendId}}.(name, relationship)',
    query_kwargs={'friendId': 'f42'}
)
removed_friend_name_value: Optional[str] = removed_values['name']
removed_friend_relationship_value: Optional[str] = removed_values['relationship']
```

### 9 - Removing multiple fields values with remove_multiple_fields
{{template::{
    'filepath': 'docs_parts/templates/grouped_fields_operation_template.md', 
    'operation_link': "[remove_multiple_fields](../api/remove_multiple_fields)",
    'type_operation_single': "remove_field", 'alteration_type': "remove",
    'object_link': "[FieldRemover](../api/FieldRemover.md)", 'additional': ""
}::}}
```python
from typing import Dict, Optional, Any
from StructNoSQL import FieldGetter

removed_values: Dict[str, Optional[Any]] = table_client.remove_multiple_fields(
    key_value='x42', getters={
        'status': FieldRemover(field_path='status'),
        'friend_relationship': FieldRemover(
            field_path='friends.{{friendId}}.relationship', 
            query_kwargs={'friendId': 'f42'}, 
        ),
        'metadata_lastLoginTimestamp': FieldRemover(
            field_path='metadata.lastLoginTimestamp', 
        )
    }
)
removed_status: Optional[str] = removed_values['status']
removed_friend_relationship: Optional[str] = removed_values['friend_relationship']
removed_last_login_timestamp: Optional[int] = removed_values['metadata_lastLoginTimestamp']
```
{{template::{
    'filepath': 'docs_parts/templates/multi_selectors_template.md',
    'variable_name': "removed_values", 'individual_target_type_name': "remover",
    'default_value': "None", 'attempted_operation_explanation': "tried to remove"
}::}}

### 10 - Removing multiple fields values with remove_multiple_fields without data validation
{{file::docs_parts/reason_for_disabling_data_validation.md::}}
```python
from typing import Dict, Optional, Any
from StructNoSQL import FieldGetter

removed_values: Dict[str, Optional[Any]] = table_client.remove_multiple_fields(
    key_value='x42', getters={
        'status': FieldGetter(field_path='status'),
        'friend_relationship': FieldGetter(
            field_path='friends.{{friendId}}.relationship', 
            query_kwargs={'friendId': 'f42'}, 
        ),
        'metadata_lastLoginTimestamp': FieldGetter(
            field_path='metadata.lastLoginTimestamp', 
        )
    }, data_validation=False  # <-- disable data_validation
)
removed_status: Optional[Any] = removed_values['status']
removed_friend_relationship: Optional[Any] = removed_values['friend_relationship']
removed_last_login_timestamp: Optional[Any] = removed_values['metadata_lastLoginTimestamp']
```