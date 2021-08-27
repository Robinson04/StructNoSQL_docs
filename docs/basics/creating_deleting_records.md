---
id: creating_deleting_records
slug: /basics/creating_deleting_records
title: Creating & deleting records
---



You have multiple operations at your disposition :

- [put_record](../api/put_record)
- [delete_record](../api/delete_record)
- [remove_record](../api/remove_record)

:::info Trying to update a non-existing record will automatically create it

When using one of the following operations :
- [update_field](../api/update_field)
- [update_field_return_old](../api/update_field_return_old)
- [update_multiple_fields](../api/update_multiple_fields)
- [update_multiple_fields_return_old](../api/update_multiple_fields_return_old)

If you try to update a record (selected by its primary key) that does not yet exist,
it will automatically be created with its primary key value and the field(s) you were
trying to update. Note that if your update operation was not updating all of the required
fields in your table model, a record could be created without all of your required fields present.

You should prefer the use of [put_record](../api/put_record) that enforces the presence of all
your required fields.
:::

### 1 - Creating a record with put_record

You can use [put_record](../api/get_field.md) to create a new record in your database.

Simply pass a dictionary of your record data to the ```record_dict_data``` parameter (in NoSQL databases, a record will 
always be a dictionary, and can never be something else, like a list).

Note that both the field defined as your ```primary_key``` field` and all of the required fields defined in your table 
model must be present in the record data, otherwise causing a failure of the operation.

```python
put_record_success: bool = table_client.put_record(
    record_dict_data={'userId': "exampleUserId", 'username': "Bob"}
)
```
If some of the required fields in your table model are missing from the ```record_dict_data``` or did not pass the data
validation, the database operation will not be executed, and a ```success``` value of ```False``` will be returned.


### 2 - Deleting a record

You can use [delete_record](../api/delete_record) to delete a single record with its primary key value.

```python
delete_record_success: bool = table_client.delete_record(
    indexes_keys_selectors={'userId': "exampleUserId"}
)
```
If the record you tried to remove did not exist, a success value of ```False``` will be returned.

### 3 - Removing a record
You can use [remove_record](../api/remove_record) to remove a single record with its primary key value (removing : 
deleting and retrieving the removed record in a single database operation)

```python
from typing import Optional

removed_record_data: Optional[dict] = table_client.remove_record(
    indexes_keys_selectors={'userId': "exampleUserId"}
)
```
If the record you tried to remove did not exist, a value of ```None``` will be returned.

### 4 - Changing a record primary key value by removing and recreating it

If you want to change the primary key value of a record, you will need to remove the record, change its primary key 
value and create a new record.
Use the [remove_record](../api/remove_record) operation showed in the above example, if the removal has succeeded, and
the ```removed_record_data``` is not None, create a new dictionary with the all the old attributes, and override the
your primary key value (in Python, when creating a new dict, make sure that the attribute you are modifying are set after 
the unpacking of your old dictionary, otherwise your old dictionary will override the attributes you are trying to modify).
You could also directly modify the ```removed_record_data``` dictionary instead of recreating a ```altered_record_data```,
but it is a better practice to separate create a new dictionary if it is for a different usage than your initial dictionary.
Then 
```python
from typing import Optional

removed_record_data: Optional[dict] = table_client.remove_record(
    indexes_keys_selectors={'userId': "oldExampleUserId"}
)
if removed_record_data is not None:
    altered_record_data: dict = {**removed_record_data, 'userId': "newExampleUserId"}
    put_new_record_success: bool = table_client.put_record(
        record_dict_data=altered_record_data
    )
    if put_new_record_success is not True:
        print("New record creation failure")
        old_record_restoration_success: bool = table_client.put_record(
            record_dict_data=removed_record_data
        )
        if old_record_restoration_success is not True:
            print("Old record has not been able to be restored")
```
The need to re-create the entirety of the record is a limitation imposed by DynamoDB, not by StructNoSQL.
