---
id: update_field
slug: /api/update_field
---

**Update a single field from your table and return the success of the operation with True or False.**

```python
update_success: bool = table_client.update_field(
    key_value=str, field_path=str, query_kwargs=Optional[dict]
)
```

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Description |
| ------------------ | :------: | :-----------------: | :---------- |
| key_name      | YES      | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_
| key_value     | YES      | Any  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| field_path    | YES      | str  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| value_to_set  | YES      | Any  | The value that will be set/update the attribute you selected with the field_path property. |
| query_kwargs  | NO       | dict | Used to pass data to populate a field_path that contains keys. See example below :



### Queried record :
```json
{
  "userId": "x42",
  "username": "Robinson"
}
```

### Code
```python
from typing import Optional

from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    username = BaseField(name='username', field_type=str, required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
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
        