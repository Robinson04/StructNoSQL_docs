---
id: delete_record
title: delete_record
slug: /api/delete_record
---

**Delete a record from the database. Return the success of the operation with True or False.**

```python
deletion_success = table.delete_record(indexes_keys_selectors=Dict[str, str])
```


## Availability

| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ✅
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ✅
| ExternalDynamoDBApiCachingTable | ✅

## Example :

todo