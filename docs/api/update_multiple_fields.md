---
id: update_multiple_fields
slug: /api/update_multiple_fields
---

**Update multiple fields values from a single record, in a single database operation.**

```python
update_success: bool = table_client.update_multiple_fields(
    key_value=str, setters=[
        FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict]),
        FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict])
    ]
)
```

:::tip Will usually be Atomic
Any setter that does not pass data validation will be discarded client side by StructNoSQL, but since all of your valid 
setters will be grouped in a single operation, if a single of your setter is invalid and cause the operation to crash, 
all of your setters will be rejected/and reverted (for example, trying to access/modify a value inside a field that 
should be a dict, where it is in reality a list)
:::

:::warning Not always Atomic !
The data validation will be ran on the entirety of your data before starting to
send database requests. As explained in [Operations Sectioning](../details/operations_sectioning.md), if the sum of the 
size of all your setters exceeds 400KB (the DynamoDB limit per operation), your request will automatically be divided 
into multiple requests. If a/some part's of your operation are executed without causing a database rejection, and then 
one of the part of your operation is rejected, you will get a success value of False from the function call, yet, the 
parts of your operation that have already been completed, will not be reverted.
:::

## Parameters
| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| key_value | YES | Any | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| setters | YES | List[[FieldSetter](../api/FieldSetter.md)] | - | A list of FieldSetter object. See [FieldSetter](../api/FieldSetter.md) |


## Availability
| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ✅
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ✅
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

from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel, FieldSetter
from typing import Optional, Dict


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
            data_model=UsersTableModel, primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

with open("record.json", 'r') as file:
    source_record_data: dict = json.load(fp=file)
    put_record_success: bool = table_client.put_record(record_dict_data=source_record_data)
    if put_record_success is not True:
        print("Error with put_record")

update_success: bool = table_client.update_multiple_fields(
    key_value='x42', setters=[
        FieldSetter(field_path='username', value_to_set='Paul'),
        FieldSetter(
            field_path='tokens.{{tokenId}}',
            query_kwargs={'tokenId': 't42'},
            value_to_set={'expirationTimestamp': '1618324660'}
        ),
        FieldSetter(field_path='lastConnectionTimestamp', value_to_set='1606714120')
    ]
)
print(f"Multi update success : {update_success}")

```

### Output
```
Multi update success : True
```
        