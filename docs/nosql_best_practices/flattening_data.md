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
{
  "userId": "x42",
  "layoutItems": {
    "item1": {
      "active": true,
      "size": 60
    },
    "item2": {
      "active": false,
      "size": 35,
      "parentId": "item1"
    },
    "item3": {
      "active": false,
      "size": 89,
      "parentId": "item2"
    }
  }
}
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

With this second approach, all our items are present in same dict, which means you should not consider using counter ids 
and instead use unique identifiers for example uuid's (read more at [Unique ids](../nosql_best_practices/unique_ids.md)).
Each item has a new non-required field, the parentId, which should contain the id of another item that should act as the
parent for your item.

This allows you to only modify a single field in your item to change its relationship, no matter the size of the item,
or even if there are other items that consider as their parent the item you are modifying.

This also gives you the ability to not be constrained by the DynamoDB depth limit of 32 (read more at 
[The depth limit](../basics/recursive_nesting.md#the-depth-limit)) since all of your items start at the same depth level.

It is then your responsibility to reconstruct your data from the flattened data either server side, or better, client 
side. You will find below two examples, one in ```Python``` and one in ```Typescript``` to efficiently reconstruct 
nested data from flattened data.


## (Python) Reconstruct nested data from flattened data


### Queried record
```json
{
  "userId": "x42",
  "layoutItems": {
    "item1": {
      "active": true,
      "size": 60
    },
    "item2": {
      "active": false,
      "size": 35,
      "parentId": "item1"
    },
    "item3": {
      "active": false,
      "size": 89,
      "parentId": "item2"
    }
  }
}
```

### Code
```python
from typing import Optional, Dict, List

flattened_layout_items: Optional[Dict[str, dict]] = table_client.get_field(
    key_value='x42', field_path='layoutItems'
)
if flattened_layout_items is not None:
    root_items: List[dict] = []
    all_items: Dict[str, dict] = {}
    children_waiting_by_parent_ids: Dict[str, Dict[str, dict]] = {}

    for item_id, item_data in flattened_layout_items.items():
        # We use the pop function instead of the get function, in order to
        # retrieve and then remove the parentId attribute if it is present.
        parent_id: Optional[str] = item_data.pop('parentId', None)
        # Note that the items in the flattened_layout_items variable will be
        # modified by the pop function, and will lose their parentId attribute.
        # If you need to re-use the data in the flattened_layout_items
        # variable, before calling the .pop function, create a new object
        # from your item_data, like so :
        # item_data = {**item_data}

        # This would be the place to perform modifications on your item data.

        all_items[item_id] = item_data
        # The all_items variable is a flattened representation of your items, which could
        # be removed and replaced by using the existing flattened_layout_items variable, but,
        # if you ended re-creating a new object from your item_data, the flattened_layout_items
        # would contain the source of your item data, and not your current item. If you were
        # potentially creating or deleting items from/to the flattened_layout_items variable,
        # since we are currently iterating over the variable itself, it could cause major issues
        # in your application, and even crash it.

        if parent_id is None:
            root_items.append(item_data)
        else:
            if parent_id not in children_waiting_by_parent_ids:
                children_waiting_by_parent_ids[parent_id] = {}
            children_waiting_by_parent_ids[parent_id][item_id] = item_data

    for parent_id, children_items in children_waiting_by_parent_ids.items():
        # All items present in the root_items list are also present in the all_items dict,
        # and point's to the same objects. So, if we modify the children key of an item from
        # the all_items variable, we will also see the change on the item from the root_items dict.
        all_items[parent_id]['children'] = children_items
        # We directly write to the 'children' key, because we did not defined a field with
        # the children key in our table model, and so we never risk to override existing data.
    print(root_items)
```

### Output
```
{
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
```
         


## (Typescript) Reconstruct nested data from flattened data

### Queried record
```json
{
  "userId": "x42",
  "layoutItems": {
    "item1": {
      "active": true,
      "size": 60
    },
    "item2": {
      "active": false,
      "size": 35,
      "parentId": "item1"
    },
    "item3": {
      "active": false,
      "size": 89,
      "parentId": "item2"
    }
  }
}
```

### code.ts
```typescript
export interface RetrievedLayoutItemData {
    active?: boolean;
    size?: boolean;
    parentId?: string;
}

export interface ClientLayoutItemData {
    active?: boolean;
    size?: boolean;
    children?: { [key: string]: ClientLayoutItemData };
}

export function reconstructData(flattenedData: { [key: string]: RetrievedLayoutItemData }): ClientLayoutItemData[] {
    const rootItems: ClientLayoutItemData[] = [];
    const allItems: { [key: string]: ClientLayoutItemData } = {};
    const childrenWaitingByParentIds: { [key: string]: { [key: string]: ClientLayoutItemData } } = {};

    for (let itemKeyId in flattenedData) {
        const retrievedItemData: RetrievedLayoutItemData = flattenedData[itemKeyId];
        const parentId: string | undefined = retrievedItemData.parentId;

        const clientItemData: ClientLayoutItemData = {
            active: retrievedItemData.active, size: retrievedItemData.size
        };
        allItems[itemKeyId] = clientItemData;

        if (parentId === undefined) {
            rootItems.push(clientItemData);
        } else {
            if (!(childrenWaitingByParentIds.hasOwnProperty(parentId))) {
                childrenWaitingByParentIds[parentId] = {};
            }
            childrenWaitingByParentIds[parentId][itemKeyId] = clientItemData;
        }
    }

    for (let parentKeyId in childrenWaitingByParentIds) {
        const childrenItems: { [key: string]: ClientLayoutItemData } = childrenWaitingByParentIds[parentKeyId];
        allItems[parentKeyId].children = childrenItems;
    }
    return rootItems;
}
const reconstructedRootItems = reconstructData(flattenedDataYouRetrievedFromYourBackend);
console.log(reconstructedRootItems);
```

### Output
```text
{
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
```

