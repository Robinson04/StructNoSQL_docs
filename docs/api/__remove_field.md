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

{{file::../parts/table_header.md}}
{{file::../parts/key_name_table_row.md}}
{{file::../parts/key_value_table_row.md}}
{{file::../parts/field_path_table_row.md}}
{{file::../parts/query_kwargs_table_row.md}}


## Multi fields selectors

{{sampler::remove_field/basic}}
 