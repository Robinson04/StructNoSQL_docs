---
id: get_multiple_fields
slug: /api/get_multiple_fields
---

**Retrieve multiple fields in one operation, from a single record selected by its primary key.**

```python
retrieved_items: Dict[str, Any] = table_client.get_multiple_fields(
    key_value=str, 
    getters={
        str: FieldGetter(field_path=str, query_kwargs=Optional[dict]),
        str: FieldGetter(field_path=str, query_kwargs=Optional[dict])
    },
    data_validation=bool = True
)
```

:::tip You can use any key for the getters
No matter the field you are trying to retrieve, you can use any key's for your getter item's. You will receive your 
results in a dictionary that use the keys of your getters, even if they are not related to the field names you requested.
:::

## Parameters

{{file::docs_parts/table_header.md}}
{{file::docs_parts/key_value_table_row.md}}
{{file::docs_parts/field_getters_table_row.md}}
{{file::docs_parts/data_validation_table_row.md}}

## Availability

{{file::docs_parts/feature_availability_table/preset_all.md}}

{{sampler::../samples/get_multiple_fields/basic}}