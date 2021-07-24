---
id: delete_record
slug: /api/delete_record
---

**Delete a record from the database. Return the success of the operation with True or False.**

```python
deletion_success: bool = table.delete_record(indexes_keys_selectors=Dict[str, str])
```

## Parameters
{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/indexes_keys_selectors_table_row.md}}
{{file::../docs_parts/data_validation_table_row.md}}

## Availability
{{file::../docs_parts/feature_availability_table/preset_all.md}}

## Example :
todo