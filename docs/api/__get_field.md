---
id: get_field
slug: /api/get_field
---

**Retrieve a single or multiple fields from a single record selected by its primary key.**

```python
retrieved_item: Optional[Any] = table_client.get_field(
    key_value=str, field_path=str, 
    query_kwargs=Optional[dict],
    data_validation=bool = True
)
```

## Parameters

{{file::docs_parts/table_header.md::}}
{{file::docs_parts/key_value_table_row.md::}}
{{file::docs_parts/field_path_table_row.md::}}
{{file::docs_parts/query_kwargs_table_row.md::}}
{{file::docs_parts/data_validation_table_row.md::}}

## Availability

{{file::docs_parts/feature_availability_table/preset_all.md::}}

## Single field retrieving
{{sampler::../samples/get_field/single_selection::}}

## Multi fields selectors

If you need to access multiple items that share the same location, you can use a multi-selector. In the ```field_path```
specify the attributes you want to retrieved by enclosing them in brackets and with a comma separating each attribute.
For example : ```myItem.(attribute1, attribute2, attribute3)```

:::tip
A single database request will be constructed and send to retrieve your multiple attributes. It is then more efficient 
to use multi selectors or the [```get_multiple_fields```](../api/get_multiple_fields.md) operation as much as you can, 
instead of sending multiple operations to your database to retrieve the data you need.
:::

You cannot use a multi-selector to get multiple fields that are not in the same location. For that use case, you need
the [```get_multiple_fields```](../api/get_multiple_fields.md) operation.


{{sampler::../samples/get_field/multi_selectors::}}
 