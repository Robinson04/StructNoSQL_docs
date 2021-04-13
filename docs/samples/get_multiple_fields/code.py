from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel, FieldGetter
from typing import Dict, Optional


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    username = BaseField(name='username', field_type=str, required=False)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(name='expirationTimestamp', field_type=int, required=True)
    tokens = BaseField(name='tokens', field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)
    lastConnectionTimestamp = BaseField(name='lastConnectionTimestamp', field_type=int, required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

response_data: Optional[dict] = table_client.get_multiple_fields(
    key_value='x42', getters={
        'name': FieldGetter(field_path='username'),
        'tokenExpiration': FieldGetter(
            field_path='tokens.{{tokenId}}.expirationTimestamp',
            query_kwargs={'tokenId': 't42'}
        ),
        'lastConnectionTimestamp': FieldGetter(field_path='lastConnectionTimestamp'),
    }
)
print(response_data)
