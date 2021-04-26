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