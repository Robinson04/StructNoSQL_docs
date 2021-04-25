---
id: update_multiple_fields
title: update_multiple_fields
sidebar_label: update_multiple_fields
slug: /api/update_multiple_fields
---

**Update multiple fields from your table with a single database operation and return the success of the 
operation with True or False.**

```python
update_success: bool = table_client.update_field(
    key_value=str, setters=[
        FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict]),
        FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict])
    ]
)
```

## To note

Since all your setters will be grouped in a single operation, if a single of your setter is invalid and cause the 
operation to crash, all of your setters will be rejected/and reverted.

:::warning Not always Atomic !
The data validation will be runned on the enterity of your data before starting to
send database requests. As explained in [Operations Sectioning](../details/operations_sectioning.md), if the sum of the 
size of all your setters exceeds 400KB (the DynamoDB limit per operation), your request will automatically be divided 
into multiple requests. If a/some part's of your operation are executed without causing a database rejection, and then 
one of the part of your operation is rejected, you will get a success value of False from the function call, yet, the 
parts of your operation that have already been completed, will not be reverted.
:::

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Description |
| ------------------ | :------: | :-----------------: | :---------- |
| key_name      | No       | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_
| key_value     | YES      | Any  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| setters       | YES      | List[FieldSetter] | A list of FieldSetter object. See [FieldSetter](../api/FieldSetter.md) |

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
from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel, FieldSetter
from typing import Optional, Dict


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
        

