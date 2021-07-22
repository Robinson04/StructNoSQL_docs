---
id: get_multiple_fields
slug: /api/get_multiple_fields
---

**Retrieve multiple fields in one operation, from a single record selected by its primary key.**

```python
retrieved_items: Dict[str, Any] = table_client.get_multiple_fields(
    key_value=str, 
    getters={
        str: FieldGetter(field_path=str, query_kwargs=Optional[dict]),
        str: FieldGetter(field_path=str, query_kwargs=Optional[dict])
    },
    data_validation=bool = True
)
```

:::tip You can use any key for the getters
No matter the field you are trying to retrieve, you can use any key's for your getter item's. You will receive your 
results in a dictionary that use the keys of your getters, even if they are not related to the field names you requested.
:::

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| key_value | YES | Any | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| getters | YES | Dict[str,&nbsp;[FieldGetter](../api/FieldGetter)] | - | A dictionary with all the fields to retrieve, and the keys that will be used for the output you will receive. |
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
from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel, FieldGetter
from typing import Dict, Optional


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(field_type=int, required=True)
    tokens = BaseField(field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)
    lastConnectionTimestamp = BaseField(field_type=int, required=False)


class UsersTable(DynamoDBBasicTable):
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
        