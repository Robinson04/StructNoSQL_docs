:::warning Not clearing the cache can create discrepancies
For example, if you delete a field, the field will right-away be deleted from the in-memory cache, and a delete 
operation will be scheduled. If you clear the pending remove operations, the in-memory cache will not be changed,
and the deleted field will still be considered as deleted in the in-memory cache, but the delete operation responsible
for actually deleting the field value, will never be sent, since you would have cleared it. If you want to avoid all
risks, use the [```clear_cached_data_and_pending_operations```](../api/clear_cached_data_and_pending_operations)
:::