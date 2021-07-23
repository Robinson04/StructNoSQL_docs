---
id: update_multiple_fields_return_old
slug: /api/update_multiple_fields_return_old
---

**Update multiple fields values from a single record and return their previous values, in a single database operation.**

```python
update_success, retrieved_old_values = table_client.update_multiple_fields_return_old(
    key_value=str, setters={
        str: FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict]),
        str: FieldSetter(field_path=str, value_to_set=Any, query_kwargs=Optional[dict])
    }
)
update_success: bool
retrieved_old_values: Optional[Dict[str, Any]]
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
{{file::../docs_parts/index_name_table_row.md}}
{{file::../docs_parts/key_value_table_row.md}}
| setters       | YES      | Dict[str,&nbsp;[FieldSetter](../api/FieldSetter.md)] | A dict of FieldSetter object. See [FieldSetter](../api/FieldSetter.md) |

## Availability

{{file::../docs_parts/feature_availability_table/preset_all.md}}

## Example

{{sampler::update_multiple_fields_return_old/basic}}

