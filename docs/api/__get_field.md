---
id: get_field
slug: /api/get_field
---

**Allow to retrieve a single or multiple fields from your table.**

```python
retrieved_item: Any = table_client.get_field(
    key_value=str, field_path=str, query_kwargs=Optional[dict]
)
```

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/key_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
{{file::../docs_parts/field_path_table_row.md}}
{{file::../docs_parts/query_kwargs_table_row.md}}


## Single field retrieving
{{sampler::get_field/single_selection}}

## Multi fields selectors

If you need to access multiple items that share the same location, you can use a multi-selector. In the ```field_path```
specify the attributes you want to retrieved by enclosing them in brackets and with a comma separating each attribute.
For example : ```myItem.(attribute1, attribute2, attribute3)```

:::tip
A single database request will be constructed and send to retrieve your multiple attributes. It is then more efficient 
to use multi selectors or the [```get_multiple_fields```](./get_multiple_fields) operation as much as you can, instead of sending multiple 
operations to your database to retrieve the data you need.
:::

You cannot use a multi-selector to get multiple fields that are not in the same location. For that use case, you need
the ```get_multiple_fields``` operation.


{{sampler::get_field/multi_selectors}}
 