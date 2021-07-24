import json
from StructNoSQL import TableDataModel, DynamoDBCachingTable, PrimaryIndex, BaseField


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)

class UsersTable(DynamoDBCachingTable):
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
    # put_record will always be executed right away, hence is not considered a pending_operation
    if put_record_success is not True:
        print("Error with put_record")

print(f"First has_pending_operations before update : {table_client.has_pending_operations()}")

update_expected_success: bool = table_client.update_field(
    key_value='x42', field_path='username', value_to_set="Paul"
)
print(f"Update expected success : {update_expected_success}")

print(f"Second has_pending_operations before clear : {table_client.has_pending_operations()}")
table_client.clear_pending_operations()
print(f"Third has_pending_operations after clear : {table_client.has_pending_operations()}")
