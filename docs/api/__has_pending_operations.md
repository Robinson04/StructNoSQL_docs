---
id: has_pending_operations
slug: /api/has_pending_operations
---

**Return a bool whether there is any update or remove operations that could be committed with the
[```commit_operations```](../api/commit_operations.md) or discarded with 
[```clear_pending_operations```](../api/clear_pending_operations.md) in your 
[```CachingTable```](../caching_table/introduction.md)**

```python
do_has_pending_operations: bool = table_client.has_pending_operations()
```

{{file::docs_parts/caching_table/operations_considered_as_update.md::}}

{{file::docs_parts/caching_table/operations_considered_as_remove.md::}}

## Parameters

has_pending_operations has no parameters.
 
## Availability

{{file::docs_parts/feature_availability_table/preset_only_caching.md::}}

## Example

{{sampler::../samples/caching_table/has_pending_operations/basic}}
