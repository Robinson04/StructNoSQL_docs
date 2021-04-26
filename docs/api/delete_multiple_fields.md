---
id: delete_multiple_fields
slug: /api/delete_multiple_fields
---

**Remove multiple fields from your table and return the removed values. Return None if the removals failed.**

```python
deletion_success: bool = table_client.delete_multiple_fields(
    key_value=str, deleters=[
        FieldRemover(field_path=str, query_kwargs=Optional[dict]),
        FieldRemover(field_path=str, query_kwargs=Optional[dict])
    ]
)
```

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Description |
| ------------------ | :------: | :-----------------: | :---------- |
| key_name      | No       | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_
| key_value     | YES      | Any  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| removers      | YES      | List[[FieldRemover](../api/FieldRemover.md)] | A list of FieldRemover's object's to select the fields to delete.


## Multi fields selectors


### Queried record
```json
{
  "userId": "x42",
  "shoppingCartItems": {
    "i42": {
      "productName": "Soluble coffee jar",
      "quantity": 8
    }
  },
  "tokens": {
    "t32": {
      "expirationTimestamp": "1618322249"
    }
  }
}
```

### Code
```python
from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel, FieldSetter, FieldRemover
from typing import Optional, Dict


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    class ShoppingCartItemModel(MapModel):
        productName = BaseField(name='productName', field_type=str, required=True)
        quantity = BaseField(name='quantity', field_type=int, required=True)
    shoppingCartItems = BaseField(name='shoppingCartItems', field_type=Dict[str, ShoppingCartItemModel], key_name='itemId', required=False)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(name='expirationTimestamp', field_type=int, required=True)
    tokens = BaseField(name='tokens', field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

removed_items_status: Optional[Dict[str, bool]] = table_client.delete_multiple_fields(
    key_value='x42', removers={
        'shoppingCartItem': FieldRemover(
            field_path='shoppingCartItems.{{itemId}}',
            query_kwargs={'itemId': 'i42'}
        ),
        'removedTokens': FieldRemover(field_path='tokens')
    }
)
print(f"Removed items status : {removed_items_status}")

```

### Output
```
Removed items status : {'shoppingCartItem': True, 'removedTokens': True}
```
        
 