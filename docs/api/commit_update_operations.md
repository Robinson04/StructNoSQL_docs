---
id: commit_update_operations
slug: /api/commit_update_operations
---

**Only commit all update operations without committing remove operations in a [```CachingTable```](../caching_table/introduction.md)**

```python
table_client.commit_update_operations()
```

:::warning This functionality is only usable in [```CachingTable```](../caching_table/introduction.md) 
:::


If there is nothing to commit, calling the commit_update_operations will not send any request to your databases.

If the size of your operations exceed the DynamoDB operations limit of 400kb, they will be sectioned and sent in 
multiple requests.

#### Operations considered as update :
- [put_record](../api/put_record.md)
- [update_field](../api/update_field.md)
- [update_multiple_fields](../api/update_multiple_fields.md)

## Parameters

commit_update_operations has no parameters.

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
    userId = BaseField(name='userId', field_type=str, required=True)
    username = BaseField(name='username', field_type=str, required=False)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(name='expirationTimestamp', field_type=int, required=True)
    tokens = BaseField(name='tokens', field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)


class UsersTable(CachingTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

expected_username_update_success: bool = table_client.update_field(
    key_value='x42', field_path='username', value_to_set='Paul'
)
print(f"Username update expected success : {expected_username_update_success}")

commit_success = table_client.commit_update_operations()
print(f"Commit success : {commit_success}")

```

### Output
```
Username update expected success : True
Commit success : True
```
        