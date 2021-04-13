---
id: update_multiple_fields
title: update_multiple_fields
sidebar_label: update_multiple_fields
slug: /api/update_multiple_fields
---

## Description
Set/update multiple distinct attributes in a single record in a single database operations. 
All of your setters will be grouped into a single database operation send in a single request to the database.
This make this function more efficient than calling multiple times the update_field.

Since all your setters will be grouped in a single operation, if a single of your setter is invalid and cause the 
operation to crash, all of your setters will be rejected/and reverted.

As long as you are setting/updating fields in the same record, you have complete flexibility, and the ability to select 
any field in any path (even complex or nested paths). All those operations will be grouped in a single database request.

:::warning Not always Atomic !
The data validation will be runned on the enterity of your data before starting to
send database requests. As explained in [Operations Sectioning](../advanced/operations_sectioning.md), if the sum of the 
size of all your setters exceeds 400KB (the DynamoDB limit per operation), your request will automatically be divided 
into multiple requests. If a/some part's of your operation are executed without causing a database rejection, and then 
one of the part of your operation is rejected, you will get a success value of False from the function call, yet, the 
parts of your operation that have already been completed, will not be reverted.
:::

## Parameters

| Property name | Required | Accepted types    | Description |
| ------------- | :------: | :---------------: | :---------- |
| key_name      | YES      | str               | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_ |
| key_value     | YES      | Any               | The record selector value for your operation. Will need to be of the same type as the type you defined the index field you specified with the key_name parameter, otherwise, you will get a DataValidation error. |
| setters       | YES      | List[FieldSetter] | A list of FieldSetter object. See [FieldSetter](../api/FieldSetter.md) |

## Example


### Queried record :
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
        
