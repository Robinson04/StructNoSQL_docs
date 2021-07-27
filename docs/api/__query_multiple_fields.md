---
id: query_multiple_fields
slug: /api/query_multiple_fields
---

**Query multiple fields from potentially multiple records from your primary or any secondary index. 
Has support for filter's and results pagination.**

```python
from StructNoSQL import QueryMetadata

records_values, query_metadata = table_client.query_multiple_fields(
    key_value: str, field_path: str, query_kwargs: Optional[dict] = None,
    index_name: Optional[str] = None,
    exclusive_start_key: Optional[Any] = None,
    pagination_records_limit: Optional[int] = None,
    filter_expression: Optional[Any] = None, 
    data_validation: bool = True
) 
records_values: Optional[Dict[str, Any]]
query_metadata: QueryMetadata
``` 

Query a field and return of tuple of the both the records_values organized in a dictionary (the keys being the primary key
value of each record), and a [query_metadata](../api/QueryMetadata) object with information needed to paginate your query. 

{{file::docs_parts/paginated_queries/this_operation_is_paginated.md::}}

You can use [paginated_query_multiple_fields](../api/paginated_query_multiple_fields.md) for a managed navigation of 
paginated results with a simple iterable.

## Parameters
{{file::docs_parts/table_header.md::}}
{{file::docs_parts/index_name_table_row.md::}}
{{file::docs_parts/key_value_table_row.md::}}
{{file::docs_parts/field_getters_table_row.md::}}
{{file::docs_parts/exclusive_start_key_table_row.md::}}
{{file::docs_parts/pagination_records_limit_table_row.md::}}
{{file::docs_parts/filter_expression_table_row.md::}}
{{file::docs_parts/data_validation_table_row.md::}}
 
## Availability
{{file::docs_parts/feature_availability_table/preset_all.md::}}

## Related pages
- [Query pagination](../basics/query_pagination)
- [QueryMetadata](../api/QueryMetadata)
- [paginated_query_multiple_fields](../api/paginated_query_multiple_fields)

## Example
{{sampler::../samples/query_multiple_fields/basic::}}
 