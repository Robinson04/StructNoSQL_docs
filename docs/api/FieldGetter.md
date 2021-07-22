---
id: FieldGetter
slug: /api/FieldGetter
---

**A constructor object to specify Field's to retrieve in various operations.**

```python
from StructNoSQL import FieldGetter
FieldGetter(field_path=str, query_kwargs=Optional[dict])
```

## Usage
- [retrieve_multiple_fields](../api/retrieve_multiple_fields.md)
- [paginated_retrieve_multiple_fields](../api/paginated_retrieve_multiple_fields.md)

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| field_path | YES | str | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| query_kwargs | NO | dict | None | Used to pass data to populate a field_path that contains keys. See example below :

 