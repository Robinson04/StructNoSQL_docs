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

| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| key_value | YES | Any | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| removers      | YES      | List[[FieldRemover](../api/FieldRemover.md)] | - | A list of FieldRemover's object's to select the fields to delete.

## Availability

| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ✅
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ✅
| ExternalDynamoDBApiCachingTable | ✅

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
            data_model=UsersTableModel, primary_index=primary_index,
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
        
 