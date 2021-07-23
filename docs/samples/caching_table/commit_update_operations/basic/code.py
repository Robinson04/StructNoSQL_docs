from typing import Dict
from StructNoSQL import TableDataModel, CachingTable, PrimaryIndex, BaseField, MapModel


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    username = BaseField(name='username', field_type=str, required=False)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(name='expirationTimestamp', field_type=int, required=True)
    tokens = BaseField(name='tokens', field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)


class UsersTable(CachingTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel, primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

expected_username_update_success: bool = table_client.update_field(
    key_value='x42', field_path='username', value_to_set='Paul'
)
print(f"Username update expected success : {expected_username_update_success}")

commit_success = table_client.commit_update_operations()
print(f"Commit success : {commit_success}")
