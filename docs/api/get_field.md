---
id: get_field
slug: /api/get_field
---

**Allow to retrieve a single or multiple fields from your table.**

```python
retrieved_item: Any = table_client.get_field(
    key_value=str, field_path=str, query_kwargs=Optional[dict]
)
```

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Description |
| ------------------ | :------: | :-----------------: | :---------- |
| key_name      | No       | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_
| key_value     | YES      | Any  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| field_path    | YES      | str  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| query_kwargs  | NO       | dict | Used to pass data to populate a field_path that contains keys. See example below :


## Single field retrieving

### Queried record
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
from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel
from typing import Dict, Optional


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class FriendModel(MapModel):
        relationshipStatus = BaseField(field_type=str, required=False)
    friends = BaseField(field_type=Dict[str, FriendModel], key_name='friendId', required=False)


class UsersTable(DynamoDBBasicTable):
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
        

## Multi fields selectors

If you need to access multiple items that share the same location, you can use a multi-selector. In the ```field_path```
specify the attributes you want to retrieved by enclosing them in brackets and with a comma separating each attribute.
For example : ```myItem.(attribute1, attribute2, attribute3)```

:::tip
A single database request will be constructed and send to retrieve your multiple attributes. It is then more efficient 
to use multi selectors or the [```get_multiple_fields```](./get_multiple_fields) operation as much as you can, instead of sending multiple 
operations to your database to retrieve the data you need.
:::

You cannot use a multi-selector to get multiple fields that are not in the same location. For that use case, you need
the ```get_multiple_fields``` operation.



### Queried record
```json
{
  "userId": "x42",
  "username": "Robinson",
  "friends": {
    "b112": {
      "name": "Malo",
      "profession": "electrical engineer",
      "score": 100
    }
  }
}
```

### Code
```python
from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel
from typing import Dict, Optional


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class FriendModel(MapModel):
        name = BaseField(field_type=str, required=False)
        profession = BaseField(field_type=str, required=False)
        score = BaseField(field_type=int, required=False)
    friends = BaseField(field_type=Dict[str, FriendModel], key_name='friendId', required=False)


class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

requested_friend_id = 'b112'
response_data: Optional[dict] = table_client.get_field(
    key_value='x42',
    field_path='friends.{{friendId}}.(name, profession, score)',
    query_kwargs={'friendId': requested_friend_id}
)
print(response_data)

```

### Output
```
{'name': 'Malo', 'profession': 'electrical engineer', 'score': 100}
```
        
 