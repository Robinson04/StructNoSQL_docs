---
id: has_pending_remove_operations
slug: /api/has_pending_remove_operations
---

**Return a bool whether there is any remove operations that could be committed with the
[```commit_remove_operations```](../api/commit_remove_operations.md) or discarded with 
[```clear_pending_remove_operations```](../api/clear_pending_remove_operations.md) in your 
[```CachingTable```](../caching_table/introduction.md)**

```python
do_has_pending_remove_operations: bool = table_client.has_pending_remove_operations()
```

{{file::../docs_parts/caching_table/operations_considered_as_remove.md}}

## Parameters

has_pending_remove_operations has no parameters.
 
## Availability

{{file::../docs_parts/feature_availability_table/preset_only_caching.md}}

## Example
{{sampler::caching_table/has_pending_remove_operations/basic}}