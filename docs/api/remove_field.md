---
id: remove_field
slug: /api/remove_field
---

## Parameters

| Property name | Required | Accepted types | Description |
| ------------- | :------: | :------------: | :---------- |
| key_name      | YES      | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_ |
| key_value     | YES      | Any  | The record selector value for your operation. Will need to be of the same type as the type you defined the index field you specified with the key_name parameter, otherwise, you will get a DataValidation error. |
| field_path    | YES      | str  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md) |
| query_kwargs  | NO       | dict | Used to pass data to populate a field_path that contains keys. See example below  : |


## Multi fields selectors


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
from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel, FieldSetter
from typing import Optional, Dict


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

removed_item: Optional[dict] = table_client.remove_field(
    key_value='x42',
    field_path='shoppingCartItems.{{itemId}}',
    query_kwargs={'itemId': 'i42'}
)
print(f"Removed item : {removed_item}")

```

### Output
```
Removed item : {'productName': "Soluble coffee jar", 'quantity': 8}
```
        
 