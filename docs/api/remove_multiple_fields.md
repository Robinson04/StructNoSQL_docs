---
id: remove_multiple_fields
slug: /api/remove_multiple_fields
---

**Remove multiple fields from your table and return the removed values. Return None if the removals failed.**

```python
removed_items: Optional[dict] = table_client.remove_multiple_fields(
    key_value=str, removers={
        str: FieldRemover(field_path=str, query_kwargs=Optional[dict]),
        str: FieldRemover(field_path=str, query_kwargs=Optional[dict])
    }
)
```

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Description |
| ------------------ | :------: | :-----------------: | :---------- |
| key_name      | No       | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_
| key_value     | YES      | Any  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| removers      | YES      | Dict[str,&nbsp;[FieldRemover](../api/FieldRemover.md)] | A dictionary with the keys that will be used to return the removed items, and the values being FieldRemover's to select the field's to remove.


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
from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel, FieldRemover
from typing import Optional, Dict


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class ShoppingCartItemModel(MapModel):
        productName = BaseField(field_type=str, required=True)
        quantity = BaseField(field_type=int, required=True)
    shoppingCartItems = BaseField(field_type=Dict[str, ShoppingCartItemModel], key_name='itemId', required=False)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(field_type=int, required=True)
    tokens = BaseField(field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)


class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

removed_items: Optional[dict] = table_client.remove_multiple_fields(
    key_value='x42', removers={
        'shoppingCartItem': FieldRemover(
            field_path='shoppingCartItems.{{itemId}}',
            query_kwargs={'itemId': 'i42'}
        ),
        'removedTokens': FieldRemover(field_path='tokens')
    }
)
print(f"Removed items : {removed_items}")

```

### Output
```
Removed item : {'shoppingCartItem': {'productName': '"Soluble coffee jar", 'quantity': 8}, 'removedTokens': {'t32': {'expirationTimestamp': "1618322249"}}
```
        
 