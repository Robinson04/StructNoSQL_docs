---
id: clearing_cache_and_operations
title: Clearing cache & operations
---

You have multiple operations at your disposition :
- [clear_cached_data_and_pending_operations](../api/clear_cached_data_and_pending_operations) showcased in [Clearing all cached data and pending operations](../caching_table/clearing_cache_and_operations#1---clearing-all-cached-data-and-pending-operations)
- [clear_cached_data](../api/clear_cached_data) showcased in [Clearing all cached data](../caching_table/clearing_cache_and_operations#2---only-clearing-the-cached-data)
- [clear_cached_data_for_record](../api/clear_cached_data_for_record) showcased in [Clearing cached data for a single record](../caching_table/clearing_cache_and_operations#3---clearing-cached-data-for-a-single-record)
- [clear_pending_operations](../api/clear_pending_operations) showcased in [Clearing all pending databases operations](../caching_table/clearing_cache_and_operations#4---clearing-all-pending-databases-operations)
- [clear_pending_update_operations](../api/clear_pending_update_operations) showcased in [Clearing update databases operations](../caching_table/clearing_cache_and_operations#5---clearing-pending-update-operations)
- [clear_pending_remove_operations](../api/clear_pending_remove_operations) showcased in [Clearing remove databases operations](../caching_table/clearing_cache_and_operations#6---clearing-pending-remove-operations)


:::info What are data discrepancies risks ?
On this page, you will see the term 'risks of data discrepancies' and how to avoid them. It is a scenario, where because 
of manipulation you did to the cache or to the pending databases operations of your table, where even if you committed all
of your pending operations, the data in your database will not correctly reflect the data in the in-memory cache of your table.

This can happen, because when an operation has been set as pending (for example, updating a field), the in-memory cache 
of your table is being updated right away to reflect the change, even before the operation is actually committed to your database. 

If you only clear your pending operations, only your cached data (or some part of it), without clearing both of them,
this open the risk to later create data discrepancies.

For example, if you had modified a field, an update operation would
have been added to the pending operations and your in-memory cache would be updated to reflect the change right away. If
you then clear the cached data without clearing the pending operations, re-retrieve the same field you updated (the operation
tasked to update it, has not been committed but still exist), the 'not up to date' field value would be re-retrieved from
your table and cached in the in-memory cache. Next time you commit your databases operations, the field would finally be
updated in your database, while your in-memory cache is still storing the 'not up to date' value.

To avoid all risks of data discrepancies, favor only using the 
[clear_cached_data_and_pending_operations](../api/clear_cached_data_and_pending_operations) function showcased below in 
[Clearing all cached data and pending operations](../caching_table/clearing_cache_and_operations#1---clearing-all-cached-data-and-pending-operations)
:::


### 1 - Clearing all cached data and pending operations
The function does not take any parameters, will never crash, and always return a result value of ```None```.

```python
table_client.clear_cached_data_and_pending_operations()
```

:::tip This function is safe from data discrepancies
This function (or its equivalent, by calling both the [clear_cached_data](../api/clear_cached_data) and 
[clear_pending_operations](../api/clear_pending_operations) functions) is highly recommended in favor of the other 
examples below, because it is the only way to be safe from data discrepancies.
:::


### 2 - Only clearing the cached data
You can use [clear_cached_data](../api/clear_cached_data) to clear all the data of all records from your table in-memory cache.

Similarly to [clear_cached_data_and_pending_operations](../api/clear_cached_data_and_pending_operations) showcased above,
this function does not take any parameters, will never crash, and always return a result value of ```None```.

```python
table_client.clear_cached_data()
```

:::warning This function can cause data discrepancies
:::


### 3 - Clearing cached data for a single record

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

:::warning This function can cause data discrepancies
:::


### 4 - Clearing all pending databases operations

If you are not familiar with pending operations, read [Caching Table (functionalities/pending_operations)](../caching_table/).

As a reminder, each time you perform an operation that does not need to be sent immediately to the database (for example,
updating a field, where the changes can be represented in the in-memory cache, and sent later to the database, unlike
retrieving a field that is not yet in the in-memory cache, where the database operation needs to be sent immediately),
the operation will be added to the 'pending operations' that will be grouped in the least amount of operations each time
you call [Commit your operations](../caching_table/committing_operations.md)

```python
table_client.clear_pending_operations()
```

:::warning This function can cause data discrepancies
:::


### 5 - Clearing pending update operations

Remove and update operations cannot be grouped together with DynamoDB. Hence, StructNoSQL separate the two.

Instead of all the operations, you can only clear the update operations with 
[clear_pending_update_operations](../api/clear_pending_update_operations)

```python
table_client.clear_pending_update_operations()
```

:::warning This function can cause data discrepancies
:::


### 6 - Clearing pending remove operations

Similarly to only clearing the update databases operations as showcased above, you can also only clear the remove 
operations with [clear_pending_remove_operations](../api/clear_pending_remove_operations).

```python
table_client.clear_pending_remove_operations()
```

:::warning This function can cause data discrepancies
:::