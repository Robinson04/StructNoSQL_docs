---
id: remove_field
slug: /api/remove_field
---

**Remove one field value from a single record and return the removed value, with a single database operation. 
Return None if the removal failed.**

```python
removed_item: Optional[dict] = table_client.remove_field(
    key_value=str, field_path=str, query_kwargs=Optional[dict],
    data_validation=bool = True
)
```

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| key_value | YES | Any | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| field_path | YES | str | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| query_kwargs | NO | dict | None | Used to pass data to populate a field_path that contains keys. See example below :
| data_validation | NO | bool | True | Whether data validation from your table model should be applied on the retrieved data. 

## Availability
| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ✅
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ✅
| ExternalDynamoDBApiCachingTable | ✅

## Example : Basic

### Queried record
```json
{
  "userId": "x42",
  "shoppingCartItems": {
    "i42": {
      "productName": "Soluble coffee jar",
      "quantity": 8,
      "maxDiscountPercent": 33
    }
  }
}
```

### Code
```python
import json
from typing import Optional, Dict
from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class ShoppingCartItemModel(MapModel):
        productName = BaseField(field_type=str, required=True)
        quantity = BaseField(field_type=int, required=True)
        maxDiscountPercent = BaseField(field_type=int, required=True)
    shoppingCartItems = BaseField(field_type=Dict[str, ShoppingCartItemModel], key_name='itemId', required=False)

class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel, primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

with open("record.json", 'r') as file:
    source_record_data: dict = json.load(fp=file)
    put_record_success: bool = table_client.put_record(record_dict_data=source_record_data)
    if put_record_success is not True:
        print("Error with put_record")

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
        

## Example : Multi-fields selector
This example shows how to use multi selectors, to specify multiple fields to remove at once in a single database 
operation without having to use the [remove_multiple_fields](../api/remove_multiple_fields.md) operation. 
Read more about multi-fields selector at [Multi-fields selectors](../basics/multi_fields_selectors). 

### Queried record
```json
{
  "userId": "x42",
  "username": "Robinson",
  "mails": {
    "m42": {
      "receivedTimestamp": 1627134011,
      "timestampForAutoAnswer": 1627252059,
      "isNotRead": true
    }
  }
}
```

### Code
```python
import json
from typing import Optional, Dict, Any
from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=True)
    class ShoppingCartItemModel(MapModel):
        receivedTimestamp = BaseField(field_type=int, required=True)
        timestampForAutoAnswer = BaseField(field_type=int, required=False)
        isNotRead = BaseField(field_type=bool, required=False)
    mails = BaseField(field_type=Dict[str, ShoppingCartItemModel], key_name='mailId', required=False)

class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel, primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

with open("record.json", 'r') as file:
    source_record_data: dict = json.load(fp=file)
    put_record_success: bool = table_client.put_record(record_dict_data=source_record_data)
    if put_record_success is not True:
        print("Error with put_record")

removed_item_attributes: Optional[Dict[str, Any]] = table_client.remove_field(
    key_value='x42',
    field_path='mails.{{mailId}}.(timestampForAutoAnswer, isNotRead)',
    query_kwargs={'mailId': 'm42'}
)
# We only remove timestampForAutoAnswer and isNotRead. We do not touch receivedTimestamp.
print(f"Removed mail attributes : {removed_item_attributes}")

```

### Output
```
Removed mail attributes : {'timestampForAutoAnswer': 1627252059, 'isNotRead': True}
```
        