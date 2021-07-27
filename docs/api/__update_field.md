---
id: update_field
slug: /api/update_field
---

**Update one field value from a single record.**

```python
update_success: bool = table_client.update_field(
    key_value=str, field_path=str, query_kwargs=Optional[dict]
)
```

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/key_value_table_row.md}}
{{file::../docs_parts/field_path_table_row.md}}
{{file::../docs_parts/value_to_set_table_row.md}}
{{file::../docs_parts/query_kwargs_table_row.md}}

## Availability

{{file::../docs_parts/feature_availability_table/preset_all.md}}

{{sampler::update_field/basic}}