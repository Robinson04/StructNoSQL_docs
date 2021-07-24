---
id: FieldSetter
slug: /api/FieldSetter
---

**A constructor object to specify Field's to update in various operations.**

```python
from StructNoSQL import FieldSetter
FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict])
```

## Usage
- [update_multiple_fields](../api/update_multiple_fields.md)
- [update_multiple_fields_return_old](../api/update_multiple_fields_return_old.md)

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/field_path_table_row.md}}
| value_to_set  | YES      | Any  | The value that will be set for the specified field_path of the setter.
{{file::../docs_parts/query_kwargs_table_row.md}}

 