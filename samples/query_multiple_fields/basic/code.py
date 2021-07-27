import json

from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, QueryMetadata, \
    GlobalSecondaryIndex, MapModel, FieldGetter
from typing import Optional, List, Generator, Tuple


class MoviesTableModel(TableDataModel):
    id = BaseField(field_type=str, required=True)
    primaryType = BaseField(field_type=str, required=True)
    name = BaseField(field_type=str, required=True)
    class RatingsModel(MapModel):
        imdb = BaseField(field_type=(int, float), required=False)
        rottentomatoes = BaseField(field_type=(int, float), required=False)
    ratings = BaseField(field_type=RatingsModel, required=False)


class MoviesTable(DynamoDBBasicTable):
    def __init__(self):
        super().__init__(
            table_name='movies-table', region_name='eu-west-2',
            data_model=MoviesTableModel,
            primary_index=PrimaryIndex(
                hash_key_name='id',
                hash_key_variable_python_type=str
            ),
            global_secondary_indexes=[
                GlobalSecondaryIndex(
                    hash_key_name='primaryType',
                    hash_key_variable_python_type=str,
                    projection_type='ALL'
                )
            ],
            auto_create_table=True
        )


table_client = MoviesTable()

with open("record.json", 'r') as file:
    source_records_data: List[dict] = json.load(fp=file)
    for source_record_item_data in source_records_data:
        put_record_success: bool = table_client.put_record(record_dict_data=source_record_item_data)
        if put_record_success is not True:
            print(f"Could not put {source_record_item_data}")


records_paginator: Generator[Tuple[Optional[dict], QueryMetadata], None, None] = (
    table_client.query_multiple_fields(
        index_name='primaryType', key_value='Thriller',
        getters={
            'name': FieldGetter(field_path='name'),
            'imdb_rating': FieldGetter(field_path='ratings.imdb')
        },
        pagination_records_limit=3
    )
)
for records_items, query_metadata in records_paginator:
    if records_items is not None:
        if len(records_items) > 0:
            print("\nHere is some thriller tv shows you might enjoy :")
            for record_primary_key_value, record_item_values in records_items.items():
                print(f"{record_item_values} (id: {record_primary_key_value})")
        else:
            print("\nNo tv shows found in response, you might have hit the end of records.")
print("\nAll tv shows have been retrieved.")
