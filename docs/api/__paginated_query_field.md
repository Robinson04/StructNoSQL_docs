---
id: paginated_query_field
slug: /api/paginated_query_field
---

**Wrapper on the [query_field](../api/query_field.md) operation, that allows to easily perform 
paginated operation with an iterable instead of manually managing the pagination.**

```python
from StructNoSQL import QueryMetadata
from typing import Generator, Tuple, Optional

records_paginator: Generator[Tuple[Optional[dict], QueryMetadata], None, None] = (
    table_client.paginated_query_field(
        index_name=Optional[str], key_value=Any,
        field_path=str, pagination_records_limit=Optional[int],
        pagination_records_limit=Optional[int] = None,
        exclusive_start_key: Optional[Any] = None,
        filter_expression=Optional[Any] = None,
        data_validation: bool = True
    )
)
for records_items, query_metadata in records_paginator:
    if records_items is not None:
        for record_primary_key_value, record_item_data in records_items.items():
            print(record_primary_key_value)
            print(record_item_data)  # do stuff
```

{{file::docs_parts/paginated_queries/query_requests_are_being_sent_as_you_call_records_paginator.md::}}

{{file::docs_parts/paginated_queries/you_can_also_use_manual_pagination.md::}}

## Parameters
{{file::docs_parts/table_header.md::}}
{{file::docs_parts/index_name_table_row.md::}}
{{file::docs_parts/key_value_table_row.md::}}
{{file::docs_parts/field_path_table_row.md::}}
{{file::docs_parts/query_kwargs_table_row.md::}}
{{file::docs_parts/exclusive_start_key_table_row.md::}}
{{file::docs_parts/pagination_records_limit_table_row.md::}}
{{file::docs_parts/data_validation_table_row.md::}}

## Availability
{{file::docs_parts/feature_availability_table/preset_all.md::}}

## Related pages
- [Query pagination](../basics/query_pagination)
- [QueryMetadata](../api/QueryMetadata)
- [query_field](../api/query_field)

## Example
{{sampler::../samples/paginated_query_field/basic::}}
 