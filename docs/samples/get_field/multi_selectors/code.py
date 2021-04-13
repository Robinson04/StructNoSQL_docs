from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel
from typing import Dict, Optional


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    class FriendModel(MapModel):
        name = BaseField(name='name', field_type=str, required=False)
        profession = BaseField(name='profession', field_type=str, required=False)
        score = BaseField(name='score', field_type=int, required=False)
    friends = BaseField(name='friends', field_type=Dict[str, FriendModel], key_name='friendId', required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

requested_friend_id = 'b112'
response_data: Optional[dict] = table_client.get_field(
    key_value='x42',
    field_path='friends.{{friendId}}.(name, profession, score)',
    query_kwargs={'friendId': requested_friend_id}
)
print(response_data)
