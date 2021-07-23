---
id: performances
title: Performances
---


### Static indexing

When first launching your application and instantiating your table client for the first time, the model of your database
will be indexed, and keeped statically in the memory of your application. 

If you re-instantiate multiple times the same table client or database models in the lifecycle of your application, 
the cached indexing of your model will be retrieved from the cache.

For that reason, you should never try to dynamically modify a TableDataModel class at runtime or the inner variables
of a table regarding its indexing. Otherwise, when instantiating multiple times the same table or model during the 
lifecycle of your application, you would re-use a previously indexing of your table, which might not reflect the current 
modified/non-modified table model.


### The fields_switch

### Performances with deeply nested fields

When indexing your table model, all of your fields paths are indexed into a flattened dictionary that will act a switch.

Consider the following model : 
```python
class TableModel(TableDataModel):
    id = BaseField(field_type=str, required=True)
    class ItemModel(MapModel):
        name = BaseField(field_type=str, required=True)
        class MetadataItemModel(MapModel):
            type = BaseField(field_type=str, required=True)
            value = BaseField(field_type=int, required=False)
        metadata = BaseField(field_type=Dict[str, MetadataItemModel], key_name='metaItemId', required=False)
    container = BaseField(field_type=Dict[str, ItemModel], key_name='itemId', required=False)
```

Which will produce a flattened switch of :

```
'id'
'container'
'container.{{itemId}}'
'container.{{itemId}}.name'
'container.{{itemId}}.metadata'
'container.{{itemId}}.metadata.{{metaItemId}}'
'container.{{itemId}}.metadata.{{metaItemId}}.type'
'container.{{itemId}}.metadata.{{metaItemId}}.value'
```

When performing an operation to your database, you directly specify the field you are targeting using their full
path access, which is immediately looked for in the fields_switch with a single operation, without any performances
differences, no matter if the field is nested or not.
