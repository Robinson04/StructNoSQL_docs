import json
from typing import Optional, Any

from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)


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

update_success, retrieved_old_value = table_client.update_field_return_old(
    key_value='x42', field_path='username', value_to_set='Paul'
)
update_success: bool
retrieved_old_value: Optional[Any]
print(f"Update success : {update_success}")
print(f"Retrieved old value : {retrieved_old_value}")

retrieved_new_username: Optional[Any] = table_client.get_field(
    key_value='x42', field_path='username'
)
print(f"New username in database : {retrieved_new_username}")
