---
id: remove_multiple_fields
slug: /api/remove_multiple_fields
---

**Remove multiple fields from your table and return the removed values. Return None if the removals failed.**

```python
removed_items: Optional[dict] = table_client.remove_multiple_fields(
    key_value=str, removers={
        str: FieldRemover(field_path=str, query_kwargs=Optional[dict]),
        str: FieldRemover(field_path=str, query_kwargs=Optional[dict])
    }
)
```

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/key_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
| removers      | YES      | Dict[str,&nbsp;[FieldRemover](../api/FieldRemover.md)] | A dictionary with the keys that will be used to return the removed items, and the values being FieldRemover's to select the field's to remove.


## Multi fields selectors

{{sampler::remove_multiple_fields/basic}}
 