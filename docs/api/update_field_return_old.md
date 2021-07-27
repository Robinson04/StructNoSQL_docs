---
id: update_field_return_old
slug: /api/update_field_return_old
---

**Update one field value from a single record and return it's previous value, in a single database operation.**

```python
update_success, retrieved_old_value = table_client.update_field_return_old(
    key_value=str, field_path=str, query_kwargs=Optional[dict], 
    value_to_set=Any, data_validation=bool = True
)
update_success: bool
retrieved_old_value: Optional[Any]
```

If the update fails (whether because the ```value_to_set``` was invalid, or because of a database error), update_success
will be ```False``` and ```retrieved_old_value``` will be None.

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| key_value | YES | Any | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| field_path | YES | str | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| query_kwargs | NO | dict | None | Used to pass data to populate a field_path that contains keys. See example below :
| value_to_set  | YES      | Any  | The value that will be set/update the attribute you selected with the field_path property. |
| data_validation | NO | bool | True | Whether data validation from your table model should be applied on the retrieved data. 

## Availability

| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ✅
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ✅
| ExternalDynamoDBApiCachingTable | ✅


### Queried record
```json
{
  "userId": "x42",
  "username": "Robinson"
}
```

### Code
```python
import json
from typing import Optional, Any

from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)


class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel, primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

with open("record.json", 'r') as file:
    source_record_data: dict = json.load(fp=file)
    put_record_success: bool = table_client.put_record(record_dict_data=source_record_data)
    if put_record_success is not True:
        print("Error with put_record")

update_success, retrieved_old_value = table_client.update_field_return_old(
    key_value='x42', field_path='username', value_to_set='Paul'
)
update_success: bool
retrieved_old_value: Optional[Any]
print(f"Update success : {update_success}")
print(f"Retrieved old value : {retrieved_old_value}")

retrieved_new_username: Optional[Any] = table_client.get_field(
    key_value='x42', field_path='username'
)
print(f"New username in database : {retrieved_new_username}")

```

### Output
```
Update success : True
Retrieved old value : Robinson
New username in database : Paul
```
        