from typing import Dict

from StructNoSQL import TableDataModel, BaseField, MapModel, DynamoDBBasicTable, PrimaryIndex


class TableModel(TableDataModel):
    id = BaseField(field_type=str, required=True)
    class ItemModel(MapModel):
        name = BaseField(field_type=str, required=True)
        class MetadataItemModel(MapModel):
            type = BaseField(field_type=str, required=True)
            value = BaseField(field_type=int, required=False)
        metadata = BaseField(field_type=Dict[str, MetadataItemModel], key_name='metaItemId', required=False)
    item1 = BaseField(field_type=Dict[str, ItemModel], key_name='itemId', required=False)


class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=TableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()
print(table_client)