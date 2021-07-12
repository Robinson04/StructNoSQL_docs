from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel, FieldSetter
from typing import Optional, Dict


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=False)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(field_type=int, required=True)
    tokens = BaseField(field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)
    lastConnectionTimestamp = BaseField(field_type=int, required=False)


class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

update_success: bool = table_client.update_multiple_fields(
    key_value='x42', setters=[
        FieldSetter(field_path='username', value_to_set='Paul'),
        FieldSetter(
            field_path='tokens.{{tokenId}}',
            query_kwargs={'tokenId': 't42'},
            value_to_set={'expirationTimestamp': '1618324660'}
        ),
        FieldSetter(field_path='lastConnectionTimestamp', value_to_set='1606714120')
    ]
)
print(f"Multi update success : {update_success}")
