---
id: FieldSetter
slug: /api/FieldSetter
---

**A constructor object to specify Field's to update in various operations.**

```python
from inoft_vocal_framework import FieldSetter
FieldSetter(field_path=Any, value_to_set=Any, query_kwargs=Optional[dict])
```

## Usage :
- [update_multiple_fields](../api/update_multiple_fields.md)

## Parameters

{{file::../parts/table_header.md}}
{{file::../parts/field_path_table_row.md}}
| value_to_set  | YES      | Any  | The value that will be set for the specified field_path of the setter.
{{file::../parts/query_kwargs_table_row.md}}

 