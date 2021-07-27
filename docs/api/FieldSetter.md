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

| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| field_path | YES | str | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| value_to_set  | YES      | Any  | The value that will be set for the specified field_path of the setter.
| query_kwargs | NO | dict | None | Used to pass data to populate a field_path that contains keys. See example below :

 