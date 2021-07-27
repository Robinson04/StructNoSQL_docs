import json
from typing import Optional, Dict, Any
from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=True)
    class ShoppingCartItemModel(MapModel):
        receivedTimestamp = BaseField(field_type=int, required=True)
        timestampForAutoAnswer = BaseField(field_type=int, required=False)
        isNotRead = BaseField(field_type=bool, required=False)
    mails = BaseField(field_type=Dict[str, ShoppingCartItemModel], key_name='mailId', required=False)

class UsersTable(DynamoDBBasicTable):
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
    if put_record_success is not True:
        print("Error with put_record")

removed_item_attributes: Optional[Dict[str, Any]] = table_client.remove_field(
    key_value='x42',
    field_path='mails.{{mailId}}.(timestampForAutoAnswer, isNotRead)',
    query_kwargs={'mailId': 'm42'}
)
# We only remove timestampForAutoAnswer and isNotRead. We do not touch receivedTimestamp.
print(f"Removed mail attributes : {removed_item_attributes}")
