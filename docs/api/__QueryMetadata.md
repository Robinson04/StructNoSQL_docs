---
id: QueryMetadata
slug: /api/QueryMetadata
---

**A container object returned by queries operations that hold the required infos to navigate trough paginated results.**

```python
from StructNoSQL import QueryMetadata
QueryMetadata(
    count=int, 
    has_reached_end=bool, 
    last_evaluated_key: Optional[dict]
)
```

Even tough you can, QueryMetadata will always be constructed and returned by queries operations. You usually should 
not have to construct the object yourself.

## Usage
- [query_field](../api/query_field)
- [query_multiple_fields](../api/query_multiple_fields)
- [paginated_query_field](../api/paginated_query_field)
- [paginated_query_multiple_fields](../api/paginated_query_multiple_fields)

## Related pages
- [Query pagination](../basics/query_pagination)

## Parameters
{{file::docs_parts/table_header.md}}
| count | YES | int | - | The number of records that have been scanned during the query operation (if some filter's have been used, the number of scanned records can actually be higher than the number of returned records_items_data).
| has_reached_end | YES | bool | - | Whether all the records that could be scanned for the specified key_value and index_name of the query operation have been scanned. Note that a query operation ends its page on the last scannable record, has_reached_end will still be False. Your query operation needs to 'exceed' the last scannable record to know that it has reached the end.
| last_evaluated_key | NO | dict | None | A dict containing information about the last evaluated key of the query operation. When has_reached_end is not True, a last evaluated key will always be returned, and will be usable as an exclusive_start_key in query operations in order to continue the query operation where it was left off (ie, paginated queries).

 