from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel
from typing import Dict, Optional


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class FriendModel(MapModel):
        name = BaseField(field_type=str, required=False)
        profession = BaseField(field_type=str, required=False)
        score = BaseField(field_type=int, required=False)
    friends = BaseField(field_type=Dict[str, FriendModel], key_name='friendId', required=False)


class UsersTable(DynamoDBBasicTable):
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
