---
id: update_multiple_fields
title: update_multiple_fields
sidebar_label: update_multiple_fields
slug: /api/update_multiple_fields
---

**Update multiple fields from your table with a single database operation and return the success of the 
operation with True or False.**

```python
update_success: bool = table_client.update_field(
    key_value=str, setters=[
        FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict]),
        FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict])
    ]
)
```

## To note

Since all your setters will be grouped in a single operation, if a single of your setter is invalid and cause the 
operation to crash, all of your setters will be rejected/and reverted.

:::warning Not always Atomic !
The data validation will be runned on the enterity of your data before starting to
send database requests. As explained in [Operations Sectioning](../details/operations_sectioning.md), if the sum of the 
size of all your setters exceeds 400KB (the DynamoDB limit per operation), your request will automatically be divided 
into multiple requests. If a/some part's of your operation are executed without causing a database rejection, and then 
one of the part of your operation is rejected, you will get a success value of False from the function call, yet, the 
parts of your operation that have already been completed, will not be reverted.
:::

## Parameters

{{file::../docs_parts/table_header.md}}
{{file::../docs_parts/key_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
| setters       | YES      | List[FieldSetter] | A list of FieldSetter object. See [FieldSetter](../api/FieldSetter.md) |

## Example

{{sampler::update_multiple_fields/basic}}

