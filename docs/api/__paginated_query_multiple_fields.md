---
id: paginated_query_multiple_fields
slug: /api/paginated_query_multiple_fields
---

**Wrapper on the [query_multiple_fields](../api/query_multiple_fields.md) operation, that allows to easily perform 
paginated operation with an iterable instead of manually managing the pagination.**

```python
from StructNoSQL import QueryMetadata
from typing import Generator, Tuple, Optional, Dict, Any

records_paginator: Generator[Tuple[Optional[Dict[str, Any]], QueryMetadata], None, None] = (
    table_client.paginated_query_field(
        index_name=Optional[str], key_value=Any,
        getters={
            str: FieldGetter(field_path=str, query_kwargs=Optional[dict]),
            str: FieldGetter(field_path=str, query_kwargs=Optional[dict])
        },
        pagination_records_limit=Optional[int] = None,
        exclusive_start_key: Optional[Any] = None,
        filter_expression=Optional[Any] = None,
        data_validation: bool = True
    )
)
for records_items, query_metadata in records_paginator:
    if records_items is not None:
        for record_primary_key_value, record_items_data in records_items.items():
            print(record_primary_key_value)
            print(record_items_data)  # do stuff
```

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/index_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
{{file::../docs_parts/field_getters_table_row.md}}
{{file::../docs_parts/exclusive_start_key_table_row.md}}
{{file::../docs_parts/pagination_records_limit_table_row.md}}
{{file::../docs_parts/data_validation_table_row.md}}


## Availability

{{file::../docs_parts/feature_availability_table/preset_all.md}}


## Basic

{{sampler::paginated_query_multiple_fields/basic}}
 