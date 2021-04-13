---
id: get_field
slug: /api/get_field
---

## Parameters

| Property name | Required | Accepted types | Description |
| ------------- | :------: | :------------: | :---------- |
| key_name      | YES      | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_ |
| key_value     | YES      | Any  | The record selector value for your operation. Will need to be of the same type as the type you defined the index field you specified with the key_name parameter, otherwise, you will get a DataValidation error. |
| field_path    | YES      | str  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md) |
| query_kwargs  | NO       | dict | Used to pass data to populate a field_path that contains keys. See example below  : |


## Single field retrieving

### Queried record :
```json
{
  "userId": "x42",
  "username": "Robinson",
  "friends": {
    "b242": {
      "relationshipStatus": "superFriend"
    },
    "b59O": {
      "relationshipStatus": "lover"
    },
    "b112": {
      "relationshipStatus": "businessPartner"
    }
  }
}
```

### Code
```python
from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel
from typing import Dict, Optional


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    class FriendModel(MapModel):
        relationshipStatus = BaseField(name='relationshipStatus', field_type=str, required=False)
    friends = BaseField(name='friends', field_type=Dict[str, FriendModel], key_name='friendId', required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

requested_friend_id = 'b112'
# Typing the response_data with Optional or with str, is purely optional.
# Use it if you consider that it will make your code clearer.
response_data: Optional[str] = table_client.get_field(
    key_value='x42',
    field_path='friends.{{friendId}}.relationshipStatus',
    query_kwargs={'friendId': requested_friend_id},
)
if response_data is None:
    print(f"Status or friend with id {requested_friend_id} not found.")
else:
    print(f"Relationship status with {requested_friend_id} is {response_data}")
```

### Output
```
Relationship status with b112 is businessPartner
```
        
 