---
id: update_multiple_fields_return_old
slug: /api/update_multiple_fields_return_old
---

**Update multiple fields values from a single record and return their previous values, in a single database operation.**

```python
update_success, retrieved_old_values = table_client.update_multiple_fields_return_old(
    key_value=str, setters={
        str: FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict]),
        str: FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict])
    },
    data_validation=bool = True
)
update_success: bool
retrieved_old_values: Optional[Dict[str, Any]]
```

{{file::docs_parts/update_multiple_fields/will_usually_be_atomic.md::}}

{{file::docs_parts/update_multiple_fields/not_always_atomic.md::}}

## Parameters
{{file::docs_parts/table_header.md::}}
{{file::docs_parts/key_value_table_row.md::}}
{{file::docs_parts/field_setters_dict_table_row.md::}}
{{file::docs_parts/data_validation_table_row.md::}}

## Availability
{{file::docs_parts/feature_availability_table/preset_all.md::}}

## Example
{{sampler::../samples/update_multiple_fields_return_old/basic::}}