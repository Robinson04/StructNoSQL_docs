---
id: delete_record
slug: /api/delete_record
---

**Delete a record from the database. Return the success of the operation with True or False.**

```python
deletion_success: bool = table.delete_record(indexes_keys_selectors=Dict[str, str])
```

## Parameters
| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| indexes_keys_selectors | YES | dict | - | The key's 'todo: finish writing that'

## Availability
| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ✅
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ✅
| ExternalDynamoDBApiCachingTable | ✅

## Example :
todo