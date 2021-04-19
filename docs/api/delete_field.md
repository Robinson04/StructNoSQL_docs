---
id: delete_field
slug: /api/delete_field
---

**Delete a single field from your table and return success of operation with True or False.**

```python
deletion_success: bool = table_client.delete_field(
    key_value=str, field_path=str, query_kwargs=Optional[dict]
)
```

Delete a single field and return a value of True or False according to the deletion success.

If you try to delete a field that does not exist, the deletion will be considered a success, and a value of True will be
returned. The deletion will fail only if an error occurred in the sending or execution of your request.

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Description |
| ------------------ | :------: | :-----------------: | :---------- |
| key_name      | YES      | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_
| key_value     | YES      | Any  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| field_path    | YES      | str  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| query_kwargs  | NO       | dict | Used to pass data to populate a field_path that contains keys. See example below :


## Basic


### Queried record :
```json
{
  "userId": "x42",
  "shoppingCartItems": {
    "i42": {
      "productName": "Soluble coffee jar",
      "quantity": 8
    }
  }
}
```

### Code
```python
from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel
from typing import Dict


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    class ShoppingCartItemModel(MapModel):
        productName = BaseField(name='productName', field_type=str, required=True)
        quantity = BaseField(name='quantity', field_type=int, required=True)
    shoppingCartItems = BaseField(name='shoppingCartItems', field_type=Dict[str, ShoppingCartItemModel], key_name='itemId', required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

deletion_success: bool = table_client.delete_field(
    key_value='x42',
    field_path='shoppingCartItems.{{itemId}}',
    query_kwargs={'itemId': 'i42'}
)
print(f"Deletion success result : {deletion_success}")

```

### Output
```
Removed item : {'productName': "Soluble coffee jar", 'quantity': 8}
```
        
 