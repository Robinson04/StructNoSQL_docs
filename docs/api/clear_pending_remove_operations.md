---
id: clear_pending_remove_operations
slug: /api/clear_pending_remove_operations
---

**Discard all pending remove operations that were scheduled to be sent to your database from your 
[```CachingTable```](../caching_table/introduction.md)**

```python
table_client.clear_pending_remove_operations()
```

:::warning Not clearing the cache can create discrepancies
For example, if you delete a field, the field will right-away be deleted from the in-memory cache, and a delete 
operation will be scheduled. If you clear the pending remove operations, the in-memory cache will not be changed,
and the deleted field will still be considered as deleted in the in-memory cache, but the delete operation responsible
for actually deleting the field value, will never be sent, since you would have cleared it. If you want to avoid all
risks, use the [```clear_cached_data_and_pending_operations```](../api/clear_cached_data_and_pending_operations)
:::

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

## Related operations
- [clear_cached_data_and_pending_operations](../api/clear_cached_data_and_pending_operations)
- [clear_pending_operations](../api/clear_pending_operations)
- [has_pending_update_operations](../api/commit_update_operations)
- [commit_update_operations](../api/commit_update_operations)


## Example

### Queried record
```json
{
  "userId": "x42",
  "username": "Robinson",
  "mails": {
    "m42": {
      "status": "not-read"
    }
  }
}
```

### Code
```python
import json
from typing import Dict, Optional
from StructNoSQL import TableDataModel, DynamoDBCachingTable, PrimaryIndex, BaseField, MapModel


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)
    class MailItemModel(MapModel):
        status = BaseField(field_type=str, required=True)
    mails = BaseField(field_type=Dict[str, MailItemModel], key_name='mailId')

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
    # put_record will always be executed right away, hence is not considered a pending_operation
    if put_record_success is not True:
        print("Error with put_record")

print(f"First has_pending_update_operations before deletion : {table_client.has_pending_update_operations()}")

deletion_expected_success: bool = table_client.delete_field(
    key_value='x42', field_path='mails.{{mailId}}', query_kwargs={'mailId': 'm42'}
)
print(f"Deletion expected success : {deletion_expected_success}")

print(f"Second has_pending_remove_operations before commit : {table_client.has_pending_remove_operations()}")

operations_commit_success: bool = table_client.commit_operations()
print(f"Operations commit success : {operations_commit_success}")

print(f"Third has_pending_remove_operations after commit : {table_client.has_pending_remove_operations()}")

```

### Output
```
First has_pending_update_operations before deletion : False
Deletion expected success : True
Second has_pending_remove_operations before commit : True
Operations commit success : True
Third has_pending_remove_operations after commit : False
```
        