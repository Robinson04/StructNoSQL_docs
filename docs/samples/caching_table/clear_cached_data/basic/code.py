import json
from typing import Any, Optional

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
table_client.debug = True
# Set debug to True to retrieve each value
# with its metadata (ie, the 'fromCache' attribute)

with open("record.json", 'r') as file:
    source_record_data: dict = json.load(fp=file)
    put_record_success: bool = table_client.put_record(record_dict_data=source_record_data)
    if put_record_success is not True:
        print("Error with put_record")

    table_client.commit_operations()
    table_client.clear_cached_data()
    # put_record will cache our data, so we need to call commit_operations to
    # make sure the record is created, then clear our cached_data a first time.

first_time_retrieved_username: Optional[Any] = table_client.get_field(
    key_value='x42', field_path='username'
)
print(f"First retrieval username value : {first_time_retrieved_username}")

second_time_retrieved_username: Optional[Any] = table_client.get_field(
    key_value='x42', field_path='username'
)
print(f"Second retrieval username value : {second_time_retrieved_username}")

table_client.clear_cached_data()  # <-- We clear the cache

third_time_retrieved_username: Optional[Any] = table_client.get_field(
    key_value='x42', field_path='username'
)
print(f"Third retrieval username value : {third_time_retrieved_username}")
