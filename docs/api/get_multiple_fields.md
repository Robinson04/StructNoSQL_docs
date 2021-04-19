---
id: get_multiple_fields
slug: /api/get_multiple_fields
---

**Allow to retrieve multiple fields from your table.**

```python
retrieved_items: Dict[str, Any] = table_client.get_multiple_fields(
    key_value=str, getters={
        str: FieldGetter(field_path=str, query_kwargs=Optional[dict]),
        str: FieldGetter(field_path=str, query_kwargs=Optional[dict])
    }
)
```

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Description |
| ------------------ | :------: | :-----------------: | :---------- |
| key_name      | YES      | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_
| key_value     | YES      | Any  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| field_path    | YES      | str  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| query_kwargs  | NO       | dict | Used to pass data to populate a field_path that contains keys. See example below :


### Queried record :
```json
{
  "userId": "x42",
  "username": "Robinson",
  "tokens": {
    "t32": {
      "expirationTimestamp": "1618322249"
    }
  },
  "lastConnectionTimestamp": "1607220132"
}
```

### Code
```python
from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel, FieldGetter
from typing import Dict, Optional


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    username = BaseField(name='username', field_type=str, required=False)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(name='expirationTimestamp', field_type=int, required=True)
    tokens = BaseField(name='tokens', field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)
    lastConnectionTimestamp = BaseField(name='lastConnectionTimestamp', field_type=int, required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

response_data: Optional[dict] = table_client.get_multiple_fields(
    key_value='x42', getters={
        'name': FieldGetter(field_path='username'),
        'tokenExpiration': FieldGetter(
            field_path='tokens.{{tokenId}}.expirationTimestamp',
            query_kwargs={'tokenId': 't42'}
        ),
        'lastConnectionTimestamp': FieldGetter(field_path='lastConnectionTimestamp'),
    }
)
print(response_data)

```

### Output
```
{'name': 'Robinson', 'tokenExpiration': '1618322249', 'score': 1607220132}
```
        