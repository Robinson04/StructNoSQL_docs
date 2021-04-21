---
id: delete_field
slug: /api/delete_field
---

**Delete a single field from your table and return success of operation with True or False.**

```python
deletion_success: bool = table_client.delete_field(
    key_value=str, field_path=str, query_kwargs=Optional[dict]
)
```

Delete a single field and return a value of True or False according to the deletion success.

If you try to delete a field that does not exist, the deletion will be considered a success, and a value of True will be
returned. The deletion will fail only if an error occurred in the sending or execution of your request.

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/key_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
{{file::../docs_parts/field_path_table_row.md}}
{{file::../docs_parts/query_kwargs_table_row.md}}


## Basic

{{sampler::delete_field/basic}}
 