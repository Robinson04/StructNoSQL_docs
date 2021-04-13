from typing import Dict

from StructNoSQL import TableDataModel, BaseField, MapModel, BasicTable, PrimaryIndex


class TableModel(TableDataModel):
    id = BaseField(name='id', field_type=str, required=True)
    class ItemModel(MapModel):
        name = BaseField(name='name', field_type=str, required=True)
        class MetadataItemModel(MapModel):
            type = BaseField(name='type', field_type=str, required=True)
            value = BaseField(name='value', field_type=int, required=False)
        metadata = BaseField(name='metadata', field_type=Dict[str, MetadataItemModel], key_name='metaItemId', required=False)
    container = BaseField(name='item1', field_type=Dict[str, ItemModel], key_name='itemId', required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=TableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()
print(table_client)