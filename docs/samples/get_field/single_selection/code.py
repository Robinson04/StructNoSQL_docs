from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel
from typing import Dict, Optional


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    class FriendModel(MapModel):
        relationshipStatus = BaseField(name='relationshipStatus', field_type=str, required=False)
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
# Typing the response_data with Optional or with str, is purely optional.
# Use it if you consider that it will make your code clearer.
response_data: Optional[str] = table_client.get_field(
    key_value='x42',
    field_path='friends.{{friendId}}.relationshipStatus',
    query_kwargs={'friendId': requested_friend_id},
)
if response_data is None:
    print(f"Status or friend with id {requested_friend_id} not found.")
else:
    print(f"Relationship status with {requested_friend_id} is {response_data}")