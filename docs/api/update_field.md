---
id: update_field
slug: /api/update_field
---

**Update one field value from a single record.**

```python
update_success: bool = table_client.update_field(
    key_value=str, field_path=str, query_kwargs=Optional[dict]
)
```

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| index_name | No | str | primary_index name of table | The index\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto.
| key_value | YES | Any | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| field_path | YES | str | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| value_to_set  | YES      | Any  | The value that will be set/update the attribute you selected with the field_path property. |
| query_kwargs | NO | dict | None | Used to pass data to populate a field_path that contains keys. See example below :

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
from typing import Optional

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

update_success: bool = table_client.update_field(
    key_value='x42', field_path='username', value_to_set='Paul'
)
print(f"Update success : {update_success}")

retrieved_new_name: Optional[str] = table_client.get_field(
    key_value='x42', field_path='username'
)
print(f"Retrieved new name : {retrieved_new_name}")

```

### Output
```
Update success : True
Retrieved new name : Paul
```
        