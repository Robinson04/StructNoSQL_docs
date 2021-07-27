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
{{file::docs_parts/table_header.md}}
{{file::docs_parts/indexes_keys_selectors_table_row.md}}
{{file::docs_parts/data_validation_table_row.md}}

## Availability
{{file::docs_parts/feature_availability_table/preset_all.md}}

## Example :
todo