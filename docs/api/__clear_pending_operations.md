---
id: clear_pending_operations
slug: /api/clear_pending_operations
---

**Discard all pending update and remove operations that were scheduled to be sent to your database from your 
[```CachingTable```](../caching_table/introduction.md)**

```python
clear_success: bool = table_client.clear_pending_operations()
```

{{file::../docs_parts/caching_table/not_clearing_cache_can_create_discrepancies.md}}

:::info The remove operations are grouped
One reason that the CachingTable's postpone your operations and set them as 'pending operations', is to group them in
the smallest number of database operations. Operations that are not necessary will be sent (for example, if you 
update the same field value twice, where only the last operation would be required to be send)
:::

{{file::../docs_parts/caching_table/operations_considered_as_remove.md}}

## Parameters

has_pending_remove_operations has no parameters.
 
## Availability

{{file::../docs_parts/feature_availability_table/preset_only_caching.md}}

## Related operations
[```clear_cached_data_and_pending_operations```](../api/clear_cached_data_and_pending_operations.md)
[```has_pending_remove_operations```](../api/commit_remove_operations.md)
[```commit_remove_operations```](../api/commit_remove_operations.md)


## Example : Basic
{{sampler::caching_table/has_pending_remove_operations/basic}}

## Example : Details

This example display various cases where the cache system will smartly optimize 
your requests, and where in some cases it can be broken by clearing pending_operations.

{{sampler::caching_table/has_pending_remove_operations/details}}

