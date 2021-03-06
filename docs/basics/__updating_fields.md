---
id: updating_fields
slug: /basics/updating_fields
title: Updating fields
---

#### If not present, all the required parent field's will be created when updating a nested field

#### Trying to update a field on a non-existing record (key_value) will create the record.


You have multiple operations at your disposition :

- [update_field](../api/update_field.md) showcased in
[Updating a single simple field](../basics/updating_fields#1---updating-a-single-simple-field) &
[Updating a nested map field](../basics/updating_fields#2---updating-a-nested-map-field) &
[Updating a nested dict field](../basics/updating_fields#3---updating-a-nested-dict-field) &
[Updating a deeply nested dict field](../basics/updating_fields#4---updating-a-deeply-nested-dict-field)
- [update_multiple_fields](../api/update_multiple_fields.md) showcased in
[Updating multiple fields at once](../basics/updating_fields#5---updating-multiple-fields-at-once)
- [update_field_return_old](../api/update_field_return_old.md) showcased in
[Updating a single field and returning its old value](../basics/updating_fields#6--updating-a-single-field-and-returning-its-old-value)
- [update_multiple_fields_return_old](../api/update_multiple_fields_return_old.md) showcased in
[Updating multiple fields at once and returning their old values](../basics/updating_fields#7--updating-multiple-fields-at-once-and-returning-their-old-values) &
[Updating multiple fields at once and returning their old values without data validation](../basics/updating_fields#8--updating-multiple-fields-at-once-and-returning-their-old-values-without-data-validation)


### Creating the table for our examples
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


### 1 - Updating a single simple field
Updating a field can only be done by selecting a record with its primary key value through the ```key_value``` parameter 
(primary key values are unique in DynamoDB). 
Specify the field you want to update with the ```field_path```.
And the value to update with ```value_to_set```.
```python
update_success: bool = table_client.update_field(
    key_value='x42', field_path='username', value_to_set="Paul"
)
```
If the value you tried to update did not conform to your table model, the data validation will fail, no database 
operation will be sent, the field will not be updated, and an ```update_success``` of ```False``` will be returned.

### 2 - Updating a nested map field
{{file::docs_parts/targeting_nested_field.md::}}
```python
import time
timestamp: int = int(time.time())
update_success: bool = table_client.update_field(
    key_value='x42', field_path='metadata.lastLoginTimestamp', value_to_set=timestamp
)
```

### 3 - Updating a nested dict field
{{template::{
    'filepath': 'docs_parts/alter_nested_item_template.md', 'alteration': "update"
}::}} 
```python
update_success: bool = table_client.update_field(
    key_value='x42', field_path='friends.{{friendId}}.name', 
    query_kwargs={'friendId': 'f42'}, value_to_set="Paul"
)
```
Defining a custom keyName value for your dictionary fields is recommended (for example, friendId), but is optional. 
By default the keyName will be the field name appended with the word 'key'. The default keyName of a field name 
'friends' would be 'friendsKey' and a field named 'achievements' would create the key 'achievementsKey'

### 4 - Updating a deeply nested dict field
You can have multiple attributes in your query_kwargs in order to navigate into deeply nested fields.
You do not need to avoid defining key names that might overlap when creating your table model, which would make you
enable to define different values for the overlapping keys in your query_kwargs. If this does happen to you, the keyName
exist purely client side, is not stored in your database, and can be changed at any time.
```python
update_success: bool = table_client.update_field(
    key_value='x42', field_path='friends.{{friendId}}.achievements.{{achievementKeyName}}', 
    query_kwargs={'friendId': 'f42', 'achievementKeyName': 'sent10Messages'}, value_to_set=True
)
```

### 5 - Updating multiple fields at once
You can use [update_multiple_fields](../api/update_multiple_fields.md) to update multiple fields at once with a single 
database operation.

Like update_field, you select the record you want to update with its primary key value passed in the ```key_value``` 
parameter.

Specify the different fields you want to update by passing a list of [FieldSetter](../api/FieldSetter.md).

Similarly to update_field, each [FieldSetter](../api/FieldSetter.md) requires a field_path and value_to_set parameter,
and has an optional query_kwargs parameter.

You can update any field at any location while they are still in the same record. All of your updates will be grouped 
in a single database operation.

If any of your setters are being 'detected' as invalid client side (ie, the value_to_set is invalid) no operation will
be sent an ```update_success``` of ```False``` will be returned.

If one of your setters fails after being sent to your database (this is rare, and the main reason is if you tried to
navigate into an existing field with an invalid value, for example trying to navigate into a field defined as a dict
in your database, but a list is present instead in your database), your setters will usually be atomic, none of them
will be executed and update_success of false will be returned. The only exception to this atomicity is if your update
operation was over 400kb in size (the max operation size of DynamoDB), in which case StructNoSQL divide your update
into multiple operations where the first part of an operation can actually have been executed and will not be rollback
if a later part of your update fails.

```python
from StructNoSQL import FieldSetter

update_success: bool = table_client.update_multiple_fields(
    key_value='x42', setters=[
        FieldSetter(field_path='username', value_to_set='Paul'),
        FieldSetter(
            field_path='friends.{{friendId}}.achievements.{{achievementKeyName}}', 
            query_kwargs={'friendId': 'f42', 'achievementKeyName': 'beenFriendSinceANameChange'}, 
            value_to_set=True
        )
    ]
)
```

### 6 : Updating a single field and returning its old value
You can use [update_field_return_old](../api/update_field_return_old.md) to update a single field value, and return its
old value, with only one database operation.

If no existing value was found in the field to update, the old_field_value will be ```None```.

All of the ways to select nested fields in the above examples can be used here.
```python
from typing import Optional

update_success, old_field_value = table_client.update_field_return_old(
    key_value='x42', field_path='username', value_to_set="Paul"
)
update_success: bool
old_field_value: Optional[str]
```
The typing of update_success and old_field_value is optional, and is done in separated lines of code, because Python 
does not support typing while unpacking a tuple. 


### 7 : Updating multiple fields at once and returning their old values

You can use [update_mutliple_fields_return_old](../api/update_mutliple_fields_return_old.md) to update a single field 
value, and return their old values, with only one database operation.

Like the previous operations, you select the record you want to update with its primary key value passed in the 
```key_value``` parameter.

Similarly to update_mutliple_fields, you use the [FieldSetter](../api/FieldSetter.md) to specify the different fields to 
update. But instead of wrapping them in a list, wrap them in a dictionary, where the keys you define will be used as the 
keys to construct the ```old_fields_values``` object in which the old field's values will be returned. Pass this 
dictionary to the ```setters``` parameter.

```python
from typing import Dict, Optional, Any
from StructNoSQL import FieldSetter
import time

new_timestamp: int = int(time.time())
update_success, old_fields_values = table_client.update_multiple_fields_return_old(
    key_value='x42', setters={
        'username': FieldSetter(field_path='username', value_to_set='Paul'),
        'friend_relationship': FieldSetter(
            field_path='friends.{{friendId}}.relationship', 
            query_kwargs={'friendId': 'f42'}, 
            value_to_set="business partner"
        ),
        'metadata_lastLoginTimestamp': FieldSetter(
            field_path='metadata.lastLoginTimestamp', 
            value_to_set=new_timestamp
        )
    }
)
update_success: bool
old_fields_values: Dict[str, Optional[Any]]

old_username: Optional[str] = old_fields_values['username']
old_friend_relationship: Optional[str] = old_fields_values['friend_relationship']
last_login_timestamp: Optional[int] = old_fields_values['metadata_lastLoginTimestamp']
```
{{template::{
    'filepath': 'docs_parts/templates/multi_selectors_template.md',
    'variable_name': "old_fields_values", 'individual_target_type_name': "field",
    'default_value': "False", 'attempted_operation_explanation': "tried to update"
}::}}

### 8 : Updating multiple fields at once and returning their old values without data validation
{{file::docs_parts/reason_for_disabling_data_validation.md::}}
```python
from typing import Dict, Optional, Any
from StructNoSQL import FieldSetter
import time

new_timestamp: int = int(time.time())
update_success, old_fields_values = table_client.update_multiple_fields_return_old(
    key_value='x42', setters={
        'username': FieldSetter(field_path='username', value_to_set='Paul'),
        'friend_relationship': FieldSetter(
            field_path='friends.{{friendId}}.relationship', 
            query_kwargs={'friendId': 'f42'}, 
            value_to_set="business partner"
        ),
        'metadata_lastLoginTimestamp': FieldSetter(
            field_path='metadata.lastLoginTimestamp', 
            value_to_set=new_timestamp
        )
    }, data_validation=False  # <-- disable data_validation
)
update_success: bool
old_fields_values: Dict[str, Optional[Any]]

old_username: Optional[Any] = old_fields_values['username']
old_friend_relationship: Optional[Any] = old_fields_values['friend_relationship']
last_login_timestamp: Optional[Any] = old_fields_values['metadata_lastLoginTimestamp']
```