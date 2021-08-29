---
id: clearing_cache_and_operations
title: Clearing cache & operations
---

You have multiple operations at your disposition :
- [clear_cached_data](../api/clear_cached_data)
- [clear_cached_data_for_record](../api/clear_cached_data_for_record)
- [clear_pending_operations](../api/clear_pending_operations)
- [clear_pending_update_operations](../api/clear_pending_update_operations)
- [clear_pending_remove_operations](../api/clear_pending_remove_operations)
- [clear_cached_data_and_pending_operations](../api/clear_cached_data_and_pending_operations)


### 1 - Clearing all cached data
You can use [clear_cached_data](../api/clear_cached_data) to clear all the cached data of all records.
The function does not take any parameters, will never crash, and always return a result value of ```None```.

```python
table_client.clear_cached_data()
```

:::warning Not clearing the cache can create discrepancies
For example, if you delete a field, the field will right-away be deleted from the in-memory cache, and a delete 
operation will be scheduled. If you clear the pending remove operations, the in-memory cache will not be changed,
and the deleted field will still be considered as deleted in the in-memory cache, but the delete operation responsible
for actually deleting the field value, will never be sent, since you would have cleared it. If you want to avoid all
risks, use the [```clear_cached_data_and_pending_operations```](../api/clear_cached_data_and_pending_operations)
:::

### 2 - Clearing all cached data and pending operations
To avoid risks of data discrepancies as explained in the above example, you should use the
[clear_cached_data_and_pending_operations](../api/clear_cached_data_and_pending_operations) function.

Similarly to [clear_cached_data](../api/clear_cached_data) showcased above, the function does not take any parameters,
will never crash, and always return a result value of ```None```.

```python
table_client.clear_cached_data_and_pending_operations()
```

### 3 - Clearing all pending databases operations

If you are not familiar with pending operations, read [Caching Table (functionalities/pending_operations)](../caching_table/).

As a reminder, each time you perform an operation that does not need to be sent immediately to the database (for example,
updating a field, where the changes can be represented in the in-memory cache, and sent later to the database, unlike
retrieving a field that is not yet in the in-memory cache, where the database operation needs to be sent immediately),
the operation will be added to the 'pending operations' that will be grouped in the least amount of operations each time
you call [Commit your operations](../caching_table/committing_operations.md)

```python
table_client.clear_pending_operations()
```

:::info This function can cause data discrepancies
When an operation has been set as pending (for example, updating a field), the in-memory cache has been updated right
away to reflect the change, even before the operation is actually committed to your database. Clearing your pending
operations without also clearing the cached data can cause scenarios where even the in-memory cache can incorrectly reflect
the actual data in your database. If you want to avoid all risks, use the 
[clear_cached_data_and_pending_operations](../api/clear_cached_data_and_pending_operations) showcased above in 
[Clearing all cached data and pending operations](../caching_table/clearing_cache_and_operations#2---clearing-all-cached-data-and-pending-operations)
:::

### 4 - Clearing update databases operations

Remove and update operations cannot be grouped together with DynamoDB. Hence, StructNoSQL separate the two.

Instead of all the operations, you can only clear the update operations with 
[clear_pending_update_operations](../api/clear_pending_update_operations)

```python
table_client.clear_pending_update_operations()
```

### 5 - Clearing remove databases operations

Similarly to only clearing the update databases operations as showcased above, you can also only clear the remove 
operations with [clear_pending_remove_operations](../api/clear_pending_remove_operations).

```python
table_client.clear_pending_remove_operations()
```

### 6 - Clearing cached data for a single record

Instead of clearing all the cached data, you can clear it for a single cached record with 
[clear_cached_data_for_record](../api/clear_cached_data_for_record).

:::info What is a cached record ?
When caching your data, StructNoSQL separate it record by record indexed with their primary key value.
Even if you queried some records based on their secondary indexes (see [Querying fields](../basics/querying_fields)), 
a CachingTable will always retrieve the primary key value of each record to properly cache the attributes you retrieved.
:::

```python
table_client.clear_cached_data_for_record(record_primary_key='exampleUserId')
```

The function does not take any parameter, always returns ```None```, and no error will be thrown if you try to clear the
cached data for a non-existing record or if he is not present in your in-memory cache.

---

Note that this will clear both the data that has been retrieved and cached, and the data that has been defined
client-side, but not yet committed to the database. This might cause issues, where you might update or delete a field, 
which will be saved client-side in the cached_data and create a pending database operation, then you would clear the
cached_data, re-retrieve the field you modified earlier, then finally commit the database operation tasked with 
modifying it. 
