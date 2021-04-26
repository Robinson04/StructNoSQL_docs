---
id: flattening-data
title: Flattening data
slug: /nosql-best-practices/flattening-data
---

If you come from a SQL background, and you need create relationships between items, or parent/child relations you might 
initially think that with NoSQL databases you do not need to create relationships between fields, and can nest your data
the same way you represent it in your application.

Let's look at two-approaches of modeling and representing the same data :

## Nested layout items (the bad approach)

### Table model
```python
from StructNoSQL import TableDataModel, MapModel, BaseField, ActiveSelf
from typing import Dict

class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    class LayoutItemModel(MapModel):
        active = BaseField(name='active', field_type=bool, required=False)
        size = BaseField(name='size', field_type=int, required=False)
        children = BaseField(name='children', field_type=Dict[str, ActiveSelf], key_name='itemChildId{i}', max_nested_depth=8, required=False)
    layoutItems = BaseField(name='layoutItems', field_type=Dict[str, LayoutItemModel], key_name='itemId', required=False)
```

### Queried record
```json
{
  "userId": "x42",
  "layoutItems": {
    "item1": {
      "active": true,
      "size": 60,
      "children": {
        "item2": {
          "active": false,
          "size": 35,
          "children": {
            "item3": {
              "active": false,
              "size": 89
            }
          }
        }
      }
    }
  }
}
```

### Moving the item3 from the item2 children's to the item1 children's
```python
removed_item: Optional[dict] = table_client.remove_field(
    key_value='x42', 
    field_path='layoutItems.{{itemId}}.children.{{itemChildId0}}.children.{{itemChildId1}}',
    query_kwargs={'itemId': "item1", 'itemChild0': "item2", 'itemChildId1': "item3"}
)
if removed_item is not None:
    reinsertion_success = table_client.update_field(
        key_value='x42', 
        field_path='layoutItems.{{itemId}}.children.{{itemChildId0}}',
        query_kwargs={'itemId': "item1", 'itemChildId0': "item3"}, 
        value_to_set=removed_item
    )
```

In order to move an item, we need to physically move it. We can accomplish that by removing the field we are interested 
in (the field will be deleted, and we will retrieve the deleted value, see [delete_field](../api/delete_field.md)), and
if there was in did an item that we have been able to remove, we will re-insert the entirety of the item in our target 
field.

Which means, that we first fully removed the item from the database, which both consume a lot of writing capacity and
brings some latency in your application if you are moving big fields. Then, you re-write the entirety of your item to
your database, which will consume double the amount of writing capacity and bring twice the latency.

This approach also bring risks if your application crashes or stops after you remove the field you want to move, but 
before your re-insert it, in which case, your data will be lost if you have not taken appropriate measures in your 
application towards this issue.

This approach also makes your sensible to the DynamoDB nesting limit of 32 levels. Notice that if you count the number 
of indentations in the queried record before reaching the 'item3', you will see there is 6 indents, which means that the
'item3' key is at a depth level of 6. You still have a lot of room before reaching the maximum depth of 32 levels, yet,
this means that you will not be able to infinitely nest fields into each others (read more at 
[The depth limit](../basics/recursive_nesting.md#the-depth-limit)).

## Flattened layout items (the good approach)

### Table model
```python
from StructNoSQL import TableDataModel, MapModel, BaseField
from typing import Dict

class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    class LayoutItemModel(MapModel):
        active = BaseField(name='active', field_type=bool, required=False)
        size = BaseField(name='size', field_type=int, required=False)
        parentId = BaseField(name='parentId', field_type=str, required=False)
    layoutItems = BaseField(name='layoutItems', field_type=Dict[str, LayoutItemModel], key_name='itemId', required=False)
```

### Queried record
```json
{{file::samples/nosql_best_practices/flattening_data/reconstruct_nested_data_from_flattened_data/record.json}}
```

### Moving the item3 from the item2 children's to the item1 children's
```python
relation_update_success: bool = table_client.update_field(
    key_value='x42', 
    field_path='layoutItems.{{itemId}}.parentId',
    query_kwargs={'itemId': "item3"}, 
    value_to_set='item1'
)
```

With this second approach, all our items are present in same dict, which means you should not consider counter ids and 
instead use unique identifiers for example uuid's (read more at [Unique ids](../nosql_best_practices/unique_ids.md)).
Each item has a new non-required field, the parentId, which should contain the id of another item that should act as the
parent for your item.
It is then your responsibility to reconstruct your data from the flattened data either server side, or better, client 
side.


## (Python) Reconstruct nested data from flattened data

{{sampler::nosql_best_practices/flattening_data/reconstruct_nested_data_from_flattened_data}} 


## (Typescript) Reconstruct nested data from flattened data

### Queried record
```json
{{file::samples/nosql_best_practices/flattening_data/reconstruct_nested_data_from_flattened_data/record.json}}
```

### code.ts
```typescript
{{file::samples/nosql_best_practices/flattening_data/reconstruct_nested_data_from_flattened_data/code.ts}}
```

### Output
```text
{{file::samples/nosql_best_practices/flattening_data/reconstruct_nested_data_from_flattened_data/output.txt}}
```

