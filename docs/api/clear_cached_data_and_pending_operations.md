---
id: clear_cached_data_and_pending_operations
slug: /api/clear_cached_data_and_pending_operations
---

**Clear all cached values for all records and discard all pending update and remove operations that were scheduled to be 
sent to your database from your [```CachingTable```](../caching_table/introduction.md)**

```python
clear_success: bool = table_client.clear_cached_data_and_pending_operations()
```

Calling this function is equivalent to calling both
[```clear_cached_data```](../api/clear_cached_data) and 
[```clear_pending_operations```](../api/clear_pending_operations).

## Parameters

clear_cached_data_and_pending_operations has no parameters.
 
## Availability

| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ⬜
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ⬜
| ExternalDynamoDBApiCachingTable | ✅

## Example

todo: add an example
