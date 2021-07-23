---
id: update_field_return_old
slug: /api/update_field_return_old
---

**Update a single field value and return it's previous value, in a single database operation.**

```python
update_success, retrieved_old_value = table_client.update_field_return_old(
    key_value=str, field_path=str, query_kwargs=Optional[dict], 
    value_to_set=Any, data_validation=bool = True
)
update_success: bool
retrieved_old_value: Optional[Any]
```

If the update fails (whether because the ```value_to_set``` was invalid, or because of a database error), update_success
will be ```False``` and ```retrieved_old_value``` will be None.

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/index_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
{{file::../docs_parts/field_path_table_row.md}}
{{file::../docs_parts/query_kwargs_table_row.md}}
{{file::../docs_parts/value_to_set_table_row.md}}
{{file::../docs_parts/data_validation_table_row.md}}

## Availability

{{file::../docs_parts/feature_availability_table/preset_all.md}}

{{sampler::update_field_return_old/basic}}