---
id: has_pending_update_operations
slug: /api/has_pending_update_operations
---

**Return a bool whether there is any update operations that could be committed with the
[```commit_update_operations```](../api/commit_update_operations.md) or discarded with 
[```clear_pending_update_operations```](../api/clear_pending_update_operations.md) in your 
[```CachingTable```](../caching_table/introduction.md)**

```python
do_has_pending_update_operations: bool = table_client.has_pending_update_operations()
```

{{file::docs_parts/caching_table/operations_considered_as_update.md::}}

## Parameters

has_pending_update_operations has no parameters.
 
## Availability

{{file::docs_parts/feature_availability_table/preset_only_caching.md::}}

## Example

{{sampler::../samples/caching_table/has_pending_update_operations/basic::}}