---
id: delete_multiple_fields
slug: /api/delete_multiple_fields
---

**Remove multiple fields from your table and return the removed values. Return None if the removals failed.**

```python
deletion_success: bool = table_client.delete_multiple_fields(
    key_value=str, deleters=[
        FieldRemover(field_path=str, query_kwargs=Optional[dict]),
        FieldRemover(field_path=str, query_kwargs=Optional[dict])
    ]
)
```

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/index_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
| removers      | YES      | List[[FieldRemover](../api/FieldRemover.md)] | A list of FieldRemover's object's to select the fields to delete.

## Availability

{{file::../docs_parts/feature_availability_table/preset_all.md}}

## Multi fields selectors

{{sampler::delete_multiple_fields/basic}}
 