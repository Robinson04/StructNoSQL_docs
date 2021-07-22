import json

from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, QueryMetadata, GlobalSecondaryIndex
from typing import Optional, List


class MoviesTableModel(TableDataModel):
    id = BaseField(field_type=str, required=True)
    primaryType = BaseField(field_type=str, required=True)
    name = BaseField(field_type=str, required=True)


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


first_records_items, first_query_metadata = table_client.query_field(
    index_name='primaryType', key_value='Thriller',
    field_path='name', pagination_records_limit=3
)
records_items: Optional[dict]
query_metadata: QueryMetadata
if first_records_items is not None:
    print("Here is 3 thriller tv shows you might enjoy :")
    for record_primary_key_value, record_movie_name in first_records_items.items():
        print(f"{record_movie_name} (id: {record_primary_key_value})")

if first_query_metadata.has_reached_end is not True:
    second_records_items, second_query_metadata = table_client.query_field(
        index_name='primaryType', key_value='Thriller',
        field_path='name', pagination_records_limit=3,
        exclusive_start_key=first_query_metadata.last_evaluated_key
    )
    print("\nHere is 3 other thriller tv shows :")
    for record_primary_key_value, record_movie_name in second_records_items.items():
        print(f"{record_movie_name} (id: {record_primary_key_value})")

    # There is only 6 records with the type 'thriller', we would expect to have reached the end of the records to scan, but when a query stop's right at the last record, it will not be considered as reaching the end. We must exceed the last record
    if second_query_metadata.has_reached_end is True:
        print("\nAll the movies have been showed")
    else:
        print("\nThere might be some remaining movies to show")
        third_records_items, third_query_metadata = table_client.query_field(
            index_name='primaryType', key_value='Thriller',
            field_path='name', pagination_records_limit=3,
            exclusive_start_key=second_query_metadata.last_evaluated_key
        )
        if third_query_metadata.has_reached_end is True:
            print(f"Now i'm really done, here all the remaining tv shows : {third_records_items}")
