from typing import Optional

from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    username = BaseField(name='username', field_type=str, required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

update_success: bool = table_client.update_field(
    key_value='x42', field_path='username', value_to_set='Paul'
)
print(f"Update success : {update_success}")

retrieved_new_name: Optional[str] = table_client.get_field(
    key_value='x42', field_path='username'
)
print(f"Retrieved new name : {retrieved_new_name}")
