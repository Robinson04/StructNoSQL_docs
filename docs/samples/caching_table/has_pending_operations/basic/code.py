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

print(f"First has_pending_operations : {table_client.has_pending_operations()}")
# At first, we of course will not have any pending operations.

expected_username_update_success: bool = table_client.update_field(
    key_value='x42', field_path='username', value_to_set='Paul'
)
# update_field is not required to be executed right away, so instead of directly
# sending a database operation, an update operation will be scheduled.
print(f"Username update expected success : {expected_username_update_success}")
print(f"Second has_pending_operations : {table_client.has_pending_operations()}")

operations_commit_success: bool = table_client.commit_operations()
print(f"Operations commit success : {operations_commit_success}")
print(f"Third has_pending_operations : {table_client.has_pending_operations()}")
# After a successful call to commit_operations, we do not have any more pending operations to send.
