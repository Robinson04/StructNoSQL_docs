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

:::info The query request's are being send as you call the records_paginator
Feel free to break out of the loop of the records_paginator, since the query requests are sent progressively only as you 
iterate over the records_paginator. This means that you call that you cannot calculate the length of records_paginator
in order to know the number of records page to except.
:::

:::tip You can also use manual pagination
Notice that the operation has support for the exclusive_start_key, and each item of the records_paginator is a tuple
containing both the records_items and the query_metadata. This allows you to start you records_paginator at a specific
point to resume from a previous query operation, and you can save the last_evaluated_key of the query_metadata's to
continue your query operation later as detailed in [query_field](../api/query_field.md)
:::

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/index_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
{{file::../docs_parts/field_path_table_row.md}}
{{file::../docs_parts/query_kwargs_table_row.md}}
{{file::../docs_parts/exclusive_start_key_table_row.md}}
{{file::../docs_parts/pagination_records_limit_table_row.md}}
{{file::../docs_parts/data_validation_table_row.md}}


## Availability

{{file::../docs_parts/feature_availability_table/preset_all.md}}


## Basic

{{sampler::paginated_query_field/basic}}
 