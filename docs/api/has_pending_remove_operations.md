---
id: has_pending_remove_operations
slug: /api/has_pending_remove_operations
---

**Return a bool whether there is any remove operations that could be committed with the
[```commit_remove_operations```](../api/commit_remove_operations.md) or discarded with 
[```clear_pending_remove_operations```](../api/clear_pending_remove_operations.md) in your 
[```CachingTable```](../caching_table/introduction.md)**

```python
do_has_pending_remove_operations: bool = table_client.has_pending_remove_operations()
```

#### Operations considered as remove:  
- [delete_record](../api/delete_record.md)
- [delete_field](../api/delete_field.md)
- [delete_multiple_fields](../api/delete_multiple_fields.md)
- [remove_field](../api/remove_field.md) (will be executed right away if the value to remove is not found in the cache)
- [remove_multiple_fields](../api/remove_multiple_fields.md) (will be executed right away if the values to remove are not found in the cache)

## Parameters

has_pending_remove_operations has no parameters.
 
## Availability

| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ⬜
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ⬜
| ExternalDynamoDBApiCachingTable | ✅

## Example


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
from StructNoSQL import TableDataModel, DynamoDBCachingTable, PrimaryIndex, BaseField


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)

class UsersTable(DynamoDBCachingTable):
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
    # Currently, put_record will always be executed right away, hence is not considered a pending_operation
    if put_record_success is not True:
        print("Error with put_record")

print(f"First has_pending_operations : {table_client.has_pending_operations()}")

expected_username_update_success: bool = table_client.update_field(
    key_value='x42', field_path='username', value_to_set='Paul'
)
print(f"Username update expected success : {expected_username_update_success}")
print(f"Second has_pending_operations : {table_client.has_pending_operations()}")

commit_success = table_client.commit_operations()
print(f"Commit success : {commit_success}")
print(f"Third has_pending_operations : {table_client.has_pending_operations()}")

```

### Output
```
First has_pending_operations : False
Username update expected success : True
Second has_pending_operations : True
Commit success : True
Third has_pending_operations : False
```
        
