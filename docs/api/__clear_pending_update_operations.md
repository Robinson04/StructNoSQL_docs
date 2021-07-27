---
id: clear_pending_update_operations
slug: /api/clear_pending_update_operations
---

**Discard all pending update operations that were scheduled to be sent to your database from your 
[```CachingTable```](../caching_table/introduction.md)**

```python
table_client.clear_pending_update_operations()
```

{{file::docs_parts/caching_table/not_clearing_cache_can_create_discrepancies.md::}}

{{file::docs_parts/caching_table/operations_considered_as_remove.md::}}

## Parameters

clear_pending_update_operations has no parameters.
 
## Availability

{{file::docs_parts/feature_availability_table/preset_only_caching.md::}}

## Related operations
- [clear_cached_data_and_pending_operations](../api/clear_cached_data_and_pending_operations.md)
- [clear_pending_operations](../api/commit_remove_operations.md)
- [clear_pending_remove_operations](../api/commit_remove_operations.md)
- [has_pending_update_operations](../api/commit_remove_operations.md)
- [commit_update_operations](../api/commit_remove_operations.md)


## Example
todo: example

