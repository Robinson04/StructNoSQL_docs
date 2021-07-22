---
id: paginated_query_multiple_fields
slug: /api/paginated_query_multiple_fields
---

**Delete a single field from your table and return success of operation with True or False.**

```python
from StructNoSQL import QueryMetadata

records_values, query_metadata = table_client.query_field(
    key_value: str, field_path: str, query_kwargs: Optional[dict] = None,
    index_name: Optional[str] = None,
    exclusive_start_key: Optional[Any] = None,
    pagination_records_limit: Optional[int] = None,
    filter_expression: Optional[Any] = None, 
    data_validation: bool = True
)
records_values: Optional[dict]
query_metadata: QueryMetadata
```

Delete a single field and return a value of True or False according to the deletion success.

If you try to delete a field that does not exist, the deletion will be considered a success, and a value of True will be
returned. The deletion will fail only if an error occurred in the sending or execution of your request.

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/index_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
{{file::../docs_parts/field_path_table_row.md}}
{{file::../docs_parts/query_kwargs_table_row.md}}


## Availability

{{file::../docs_parts/feature_availability_table/preset_all.md}}


## Basic

{{sampler::delete_field/basic}}
 