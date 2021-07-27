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
    },
    data_validation=bool = True
)
update_success: bool
retrieved_old_values: Optional[Dict[str, Any]]
```

:::tip Will usually be Atomic
Any setter that does not pass data validation will be discarded client side by StructNoSQL, but since all of your valid 
setters will be grouped in a single operation, if a single of your setter is invalid and cause the operation to crash, 
all of your setters will be rejected/and reverted (for example, trying to access/modify a value inside a field that 
should be a dict, where it is in reality a list)
:::

:::warning Not always Atomic !
The data validation will be ran on the entirety of your data before starting to
send database requests. As explained in [Operations Sectioning](../details/operations_sectioning.md), if the sum of the 
size of all your setters exceeds 400KB (the DynamoDB limit per operation), your request will automatically be divided 
into multiple requests. If a/some part's of your operation are executed without causing a database rejection, and then 
one of the part of your operation is rejected, you will get a success value of False from the function call, yet, the 
parts of your operation that have already been completed, will not be reverted.
:::

## Parameters
| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| key_value | YES | Any | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| setters | YES | Dict[str,&nbsp;[FieldSetter](../api/FieldSetter.md)] | - | A dict of FieldSetter object. See [FieldSetter](../api/FieldSetter.md) |
| data_validation | NO | bool | True | Whether data validation from your table model should be applied on the retrieved data. 

## Availability
| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ✅
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ✅
| ExternalDynamoDBApiCachingTable | ✅

## Example

### Queried record
```json
{
  "userId": "x42",
  "username": "Robinson",
  "mails": {
    "m42": {
      "status": "not-read"
    }
  }
}
```

### Code
```python
import json
from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel, FieldSetter
from typing import Optional, Dict, Any


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)
    class MailItemModel(MapModel):
        status = BaseField(field_type=str, required=True)
    mails = BaseField(field_type=Dict[str, MailItemModel], key_name='mailId')

class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel, primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

with open("record.json", 'r') as file:
    source_record_data: dict = json.load(fp=file)
    put_record_success: bool = table_client.put_record(record_dict_data=source_record_data)
    if put_record_success is not True:
        print("Error with put_record")

update_success, retrieved_old_values = table_client.update_multiple_fields_return_old(
    key_value='x42', setters={
        'name': FieldSetter(field_path='username', value_to_set='Paul'),
        'old_mail_status': FieldSetter(
            field_path='mails.{{mailId}}',
            query_kwargs={'mailId': 'm42'},
            value_to_set={'status': 'read'}
        ),
    }
)
update_success: bool
retrieved_old_values: Optional[Dict[str, Any]]
print(f"Multi update success : {update_success}")
print(f"Retrieved old values : {retrieved_old_values}")

```

### Output
```
Multi update success : True
Retrieved old values : {'name': 'Robinson', 'old_mail_status': {'status': 'not-read'}}
```
        