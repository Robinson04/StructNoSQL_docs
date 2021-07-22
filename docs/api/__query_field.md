---
id: query_field
slug: /api/query_field
---

**Query a single field from potentially multiple records from your primary or any secondary index. 
Has support for filter's and results pagination.**

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

Query a field and return of tuple of the both the records_values organized in a dictionary (the keys being the primary key
value of each record), and a query_metadata object with information needed to paginate your query. 

:::info What's the request pagination ?
When the number of records you specified in pagination_records_limit have been scanned, or as soon as the data that you
will be returned reached 1MB of size, the result will be returned.
This might happen before all of the records matching your key_value and index_name have been scanned, in which case
query_metadata will contains information on how to continue your request where you left off.
:::
 
## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/index_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
{{file::../docs_parts/field_path_table_row.md}}
{{file::../docs_parts/query_kwargs_table_row.md}}
{{file::../docs_parts/exclusive_start_key_table_row.md}}
{{file::../docs_parts/pagination_records_limit_table_row.md}}
{{file::../docs_parts/filter_expression_table_row.md}}
{{file::../docs_parts/data_validation_table_row.md}}
 
## Availability

{{file::../docs_parts/feature_availability_table/preset_all.md}}

## Basic

{{sampler::query_field/pagination}}
 