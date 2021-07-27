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
