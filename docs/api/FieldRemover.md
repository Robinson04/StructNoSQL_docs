---
id: FieldRemover
slug: /api/FieldRemover
---

**A constructor object to specify Field's to remove or delete in various operations.**

```python
from StructNoSQL import FieldRemover
FieldRemover(field_path=str, query_kwargs=Optional[dict])
```

## Usage
- [delete_multiple_fields](../api/delete_multiple_fields.md)
- [remove_multiple_fields](../api/remove_multiple_fields.md)

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| field_path | YES | str | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| query_kwargs | NO | dict | None | Used to pass data to populate a field_path that contains keys. See example below :

 