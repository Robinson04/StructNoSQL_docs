---
id: get_multiple_fields
slug: /api/get_multiple_fields
---

## Parameters

| Property name | Required | Accepted types | Description |
| ------------- | :------: | :------------: | :---------- |
| key_name      | YES      | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_ |
| key_value     | YES      | Any  | The record selector value for your operation. Will need to be of the same type as the type you defined the index field you specified with the key_name parameter, otherwise, you will get a DataValidation error. |
| field_path    | YES      | str  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md) |
| query_kwargs  | NO       | dict | Used to pass data to populate a field_path that contains keys. See example below  : |


### `key_name` 
#### [string] -- [REQUIRED]

The key_name of the primary or secondary index that will be used to find the record you want to 
perform the operation onto. It will usually be the primary index field (like userId or id) that you defined.

_Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_

### `key_value` [string | int | float] -- <br/>[REQUIRED]

The record selector value for your operation. Will need to be of the same type as the type you defined the 
index field you specified with the key_name parameter, otherwise, you will get a DataValidation error.

### `field_path` [string] -- <br/>[REQUIRED]

The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)

### `value_to_set` [Any] -- <br/>[REQUIRED]
The value that will be set/update the attribute you selected with the field_path property.

### `query_kwargs` [dict]
Used to pass data to populate a field_path that contains keys. For example :

### query_kwargs example usage
```python
from StructNoSQL import TableDataModel, BaseField, MapModel
from typing import Dict

class UsersTableModel(TableDataModel):
    accountId = BaseField(name='userId', field_type=str, required=True)
    username = BaseField(name='username', field_type=str, required=False)
    class FriendModel(MapModel):
        relationshipStatus = BaseField(name='relationshipStatus', field_type=str, required=False)
    friends = BaseField(name='friends', field_type=Dict[str, FriendModel], index_name='friendId', required=False)

# Load your table model inside a table client in order to perform any operation
success = table_client.update_field(
    index_name='userId', key_value='exampleUserId',
    field_path='friends.{{friendId}}.relationshipStatus',
    query_kwargs={'friendId': 'exampleFriendId'},
    value_to_set='superFriend'
)
```



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
        



