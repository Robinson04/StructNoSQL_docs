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

{{file::docs_parts/table_header.md::}}
{{file::docs_parts/key_value_table_row.md::}}
{{file::docs_parts/field_path_table_row.md::}}
{{file::docs_parts/query_kwargs_table_row.md::}}
{{file::docs_parts/data_validation_table_row.md::}}

## Availability
{{file::docs_parts/feature_availability_table/preset_all.md::}}

## Example : Basic
{{sampler::../samples/remove_field/basic::}}

## Example : Multi-fields selector
This example shows how to use multi selectors, to specify multiple fields to remove at once in a single database 
operation without having to use the [remove_multiple_fields](../api/remove_multiple_fields.md) operation. 
Read more about multi-fields selector at [Multi-fields selectors](../basics/multi_fields_selectors). 
{{sampler::../samples/remove_field/multi-fields-selector::}}