from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel, FieldSetter, FieldRemover
from typing import Optional, Dict


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    class ShoppingCartItemModel(MapModel):
        productName = BaseField(name='productName', field_type=str, required=True)
        quantity = BaseField(name='quantity', field_type=int, required=True)
    shoppingCartItems = BaseField(name='shoppingCartItems', field_type=Dict[str, ShoppingCartItemModel], key_name='itemId', required=False)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(name='expirationTimestamp', field_type=int, required=True)
    tokens = BaseField(name='tokens', field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

removed_items: Optional[dict] = table_client.remove_multiple_fields(
    key_value='x42', removers={
        'shoppingCartItem': FieldRemover(
            field_path='shoppingCartItems.{{itemId}}',
            query_kwargs={'itemId': 'i42'}
        ),
        'removedTokens': FieldRemover(field_path='tokens')
    }
)
print(f"Removed items : {removed_items}")
