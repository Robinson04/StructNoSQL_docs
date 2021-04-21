---
id: get_multiple_fields
slug: /api/get_multiple_fields
---

**Allow to retrieve multiple fields from your table.**

```python
retrieved_items: Dict[str, Any] = table_client.get_multiple_fields(
    key_value=str, getters={
        str: FieldGetter(field_path=str, query_kwargs=Optional[dict]),
        str: FieldGetter(field_path=str, query_kwargs=Optional[dict])
    }
)
```

## Parameters

{{file::../parts/table_header.md}}
{{file::../parts/key_name_table_row.md}}
{{file::../parts/key_value_table_row.md}}
{{file::../parts/field_path_table_row.md}}
{{file::../parts/query_kwargs_table_row.md}}

{{sampler::get_multiple_fields/basic}}