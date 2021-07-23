---
id: clear_pending_update_operations
slug: /api/clear_pending_update_operations
---

**Discard all pending update operations that were scheduled to be sent to your database from your 
[```CachingTable```](../caching_table/introduction.md)**

```python
clear_success: bool = table_client.clear_pending_update_operations()
```

:::warning Not clearing the cache can create discrepancies
For example, if you delete a field, the field will right-away be deleted from the in-memory cache, and a delete 
operation will be scheduled. If you clear the pending remove operations, the in-memory cache will not be changed,
and the deleted field will still be considered as deleted in the in-memory cache, but the delete operation responsible
for actually deleting the field value, will never be sent, since you would have cleared it. If you want to avoid all
risks, use the [```clear_cached_data_and_pending_operations```](../api/clear_cached_data_and_pending_operations)
:::

#### Operations considered as remove:  
- [delete_record](../api/delete_record.md)
- [delete_field](../api/delete_field.md)
- [delete_multiple_fields](../api/delete_multiple_fields.md)
- [remove_field](../api/remove_field.md) (will be executed right away if the value to remove is not found in the cache)
- [remove_multiple_fields](../api/remove_multiple_fields.md) (will be executed right away if the values to remove are not found in the cache)

## Parameters

clear_pending_update_operations has no parameters.
 
## Availability

| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ⬜
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ⬜
| ExternalDynamoDBApiCachingTable | ✅

## Related operations
- [clear_cached_data_and_pending_operations](../api/clear_cached_data_and_pending_operations.md)
- [clear_pending_operations](../api/commit_remove_operations.md)
- [clear_pending_remove_operations](../api/commit_remove_operations.md)
- [has_pending_update_operations](../api/commit_remove_operations.md)
- [commit_update_operations](../api/commit_remove_operations.md)


## Example
todo: example

