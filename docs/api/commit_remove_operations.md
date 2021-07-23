---
id: commit_remove_operations
slug: /api/commit_remove_operations
---

**Only commit all remove operations without committing update operations in a [```CachingTable```](../caching_table/introduction.md)**

```python
table_client.commit_remove_operations()
```

:::warning This functionality is only usable in [```CachingTable```](../caching_table/introduction.md) 
:::


If there is nothing to commit, calling the commit_remove_operations will not send any request to your databases.

If the size of your operations exceed the DynamoDB operations limit of 400kb, they will be sectioned and sent in 
multiple requests.

#### Operations considered as remove:  
- [delete_record](../api/delete_record.md)
- [delete_field](../api/delete_field.md)
- [delete_multiple_fields](../api/delete_multiple_fields.md)
- [remove_field](../api/remove_field.md) (will be executed right away if the value to remove is not found in the cache)
- [remove_multiple_fields](../api/remove_multiple_fields.md) (will be executed right away if the values to remove are 
  not found in the cache)

## Parameters

commit_remove_operations has no parameters.

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
  "username": "Robinson",
  "tokens": {
    "t32": {
      "expirationTimestamp": "1618322249"
    }
  }
}
```

### Code
```python
from typing import Dict
from StructNoSQL import TableDataModel, CachingTable, PrimaryIndex, BaseField, MapModel


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(field_type=int, required=True)
    tokens = BaseField(field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)


class UsersTable(CachingTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel, primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

expected_token_deletion_success: bool = table_client.delete_field(
    key_value='x42', field_path='username'
)
print(f"Token deletion expected success : {expected_token_deletion_success}")

commit_success = table_client.commit_remove_operations()
print(f"Commit success : {commit_success}")
```

### Output
```
Token deletion expected success : True
Commit success : True
```
        