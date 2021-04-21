---
id: update_field
slug: /api/update_field
---

**Update a single field from your table and return the success of the operation with True or False.**

```python
update_success: bool = table_client.update_field(
    key_value=str, field_path=str, query_kwargs=Optional[dict]
)
```

## Parameters

{{file::../parts/table_header.md}}
{{file::../parts/key_name_table_row.md}}
{{file::../parts/key_value_table_row.md}}
{{file::../parts/field_path_table_row.md}}
| value_to_set  | YES      | Any  | The value that will be set/update the attribute you selected with the field_path property. |
{{file::../parts/query_kwargs_table_row.md}}


{{sampler::update_field/basic}}