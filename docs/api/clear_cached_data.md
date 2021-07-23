---
id: clear_cached_data
slug: /api/clear_cached_data
---

**Clear all cached values for all records in a [```CachingTable```](../caching_table/introduction.md)**

```python
table_client.clear_cached_data()
```

## Parameters

clear_cached_data has no parameters.
 
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

expected_username_update_success: bool = table_client.update_field(
    key_value='x42', field_path='username', value_to_set='Paul'
)
print(f"Username update expected success : {expected_username_update_success}")

expected_token_deletion_success: bool = table_client.delete_field(
    key_value='x42', field_path='username'
)
print(f"Token deletion expected success : {expected_token_deletion_success}")

commit_success = table_client.commit_operations()
print(f"Commit success : {commit_success}")
# Since the update_field and delete_field operations does not require to immediately
# retrieve a field from the database, the operations are actually sent to the database,
# only at this point when calling the commit_operations function.
```

### Output
```
Username update expected success : True
Token deletion expected success : True
Commit success : True
```
        
