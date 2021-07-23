import json
from typing import Dict, Optional
from StructNoSQL import TableDataModel, DynamoDBCachingTable, PrimaryIndex, BaseField, MapModel


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)
    class MailItemModel(MapModel):
        status = BaseField(field_type=str, required=True)
    mails = BaseField(field_type=Dict[str, MailItemModel], key_name='mailId')

class UsersTable(DynamoDBCachingTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel, primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()
table_client.debug = True

with open("record.json", 'r') as file:
    source_record_data: dict = json.load(fp=file)
    put_record_success: bool = table_client.put_record(record_dict_data=source_record_data)
    # Currently, put_record will always be executed right away, hence is not considered a pending_operation
    if put_record_success is not True:
        print("Error with put_record")

print(f"First has_pending_update_operations : {table_client.has_pending_update_operations()}")

removed_mail_item_value: Optional[dict] = table_client.remove_field(
    key_value='x42', field_path='mails.{{mailId}}', query_kwargs={'mailId': 'm42'}
)
print(removed_mail_item_value)
# Since

print(f"Second has_pending_remove_operations : {table_client.has_pending_remove_operations()}")
table_client.clear_pending_remove_operations()

mail_item_expected_deletion_success: bool = table_client.delete_field(
    key_value='x42', field_path='mails.{{mailId}}', query_kwargs={'mailId': 'm42'}
)
print(f"mail_item_expected_deletion_success : {mail_item_expected_deletion_success}")
print(f"Third has_pending_remove_operations : {table_client.has_pending_remove_operations()}")

table_client.clear_cached_data()
removed_value: Optional[dict] = table_client.remove_field(
    key_value='x42', field_path='mails.{{mailId}}', query_kwargs={'mailId': 'm42'}
)
print(f"removed_value : {removed_value}")
print(f"Fourth has_pending_remove_operations : {table_client.has_pending_remove_operations()}")
