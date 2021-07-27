---
id: update_multiple_fields
slug: /api/update_multiple_fields
---

**Update multiple fields values from a single record, in a single database operation.**

```python
update_success: bool = table_client.update_multiple_fields(
    key_value=str, setters=[
        FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict]),
        FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict])
    ]
)
```

{{file::docs_parts/update_multiple_fields/will_usually_be_atomic.md}}

{{file::docs_parts/update_multiple_fields/not_always_atomic.md}}

## Parameters
{{file::docs_parts/table_header.md}}
{{file::docs_parts/key_value_table_row.md}}
{{file::docs_parts/field_setters_list_table_row.md}}

## Availability
{{file::docs_parts/feature_availability_table/preset_all.md}}

## Example
{{sampler::../samples/update_multiple_fields/basic}}