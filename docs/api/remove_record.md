---
id: remove_record
slug: /api/remove_record
---

**Delete a record from the database and returned its removed values, in a single database operation.**

```python
from typing import Optional

removed_record_data: Optional[dict] = table.remove_record(
    indexes_keys_selectors=Dict[str, str],
    data_validation: bool = True
)
```

## Parameters
| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| indexes_keys_selectors | YES | dict | - | The key's
| data_validation | NO | bool | True | Whether data validation from your table model should be applied on the retrieved data. 

## Availability
| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ✅
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ✅
| ExternalDynamoDBApiCachingTable | ✅

## Example :
todo