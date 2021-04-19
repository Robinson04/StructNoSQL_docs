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

| Property&nbsp;name | Required | Accepted&nbsp;types | Description |
| ------------------ | :------: | :-----------------: | :---------- |
| field_path    | YES      | str  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| value_to_set  | YES      | Any  | The value that will be set for the specified field_path of the setter.
| query_kwargs  | NO       | dict | Used to pass data to populate a field_path that contains keys. See example below :

 