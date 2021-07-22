---
id: remove_field
slug: /api/remove_field
---

**Remove a single field from your table and return the removed value with a single database operation. 
Return None if the removal failed.**

```python
removed_item: Optional[dict] = table_client.remove_field(
    key_value=str, field_path=str, query_kwargs=Optional[dict]
)
```

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/index_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
{{file::../docs_parts/field_path_table_row.md}}
{{file::../docs_parts/query_kwargs_table_row.md}}

## Availability

{{file::../docs_parts/feature_availability_table/preset_all.md}}

## Multi fields selectors

{{sampler::remove_field/basic}}
 