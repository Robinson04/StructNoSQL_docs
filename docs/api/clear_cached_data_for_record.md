---
id: clear_cached_data_for_record
slug: /api/clear_cached_data_for_record
---

**Clear all cached values for a single record selected by its primary key value in your [```CachingTable```](../caching_table/introduction.md)**

```python
table_client.clear_cached_data_for_record(record_primary_key=str)
```

## Parameters

| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| record_primary_key | YES | str | - | The key_value of the primary_index of the record for which to clear its cached data. |
 
## Availability

| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ⬜
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ⬜
| ExternalDynamoDBApiCachingTable | ✅

## Example


### Queried record
```json
[
  {
    "id": "b12",
    "name": "Breaking Bad",
    "primaryType": "Thriller",
    "ratings": {
      "imdb": 9.4,
      "rottentomatoes": null
    }
  },
  {
    "id": "c30",
    "name": "Game of Thrones",
    "primaryType": "Fantasy",
    "ratings": {
      "imdb": 9.2,
      "rottentomatoes": null
    }
  },
  {
    "id": "d52",
    "name": "Hannibal",
    "primaryType": "Thriller",
    "ratings": {
      "imdb": 8.5,
      "rottentomatoes": null
    }
  }
]
```

### Code
```python
import json
from typing import Dict, List, Optional, Any, Union
from StructNoSQL import TableDataModel, DynamoDBCachingTable, PrimaryIndex, BaseField, MapModel, GlobalSecondaryIndex, QueryMetadata


class MoviesTableModel(TableDataModel):
    id = BaseField(field_type=str, required=True)
    primaryType = BaseField(field_type=str, required=True)
    name = BaseField(field_type=str, required=True)
    class RatingsModel(MapModel):
        imdb = BaseField(field_type=(int, float), required=False)
        rottentomatoes = BaseField(field_type=(int, float), required=False)
    ratings = BaseField(field_type=RatingsModel, required=False)


class MoviesTable(DynamoDBCachingTable):
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
table_client.debug = True

with open("record.json", 'r') as file:
    source_records_data: List[dict] = json.load(fp=file)
    for source_record_item_data in source_records_data:
        put_record_success: bool = table_client.put_record(record_dict_data=source_record_item_data)
        if put_record_success is not True:
            print(f"Could not put {source_record_item_data}")
    table_client.clear_cached_data()


records_items, query_metadata = table_client.query_field(
    index_name='primaryType', key_value='Thriller', field_path='(name, ratings)'
)
records_items: Optional[Dict[str, Any]]
query_metadata: QueryMetadata
if records_items is not None:
    print(f"Retrieved tv shows : {records_items}")

    tv_shows_names_to_primary_key_values: Dict[str, str] = {}
    for record_primary_key_value, record_item_data in records_items.items():
        record_item_tv_show_name_value: str = record_item_data['name']['value']
        tv_shows_names_to_primary_key_values[record_item_tv_show_name_value] = record_primary_key_value
    print(f"TV shows names to keys : {tv_shows_names_to_primary_key_values}")

    breaking_bad_tv_show_record_key_value: Optional[str] = tv_shows_names_to_primary_key_values.get("Breaking Bad", None)
    if breaking_bad_tv_show_record_key_value is None:
        raise Exception("Did not found the 'Breaking bad' tv show")
    hannibal_tv_show_record_key_value: Optional[str] = tv_shows_names_to_primary_key_values.get("Hannibal", None)
    if hannibal_tv_show_record_key_value is None:
        raise Exception("Did not found the 'Hannibal' tv show")

    table_client.clear_cached_data_for_record(record_primary_key=breaking_bad_tv_show_record_key_value)
    # Clear all cached data for 'Breaking Bad'

    retrieved_breaking_bad_tv_show_imdb_rating: Optional[Union[int, float]] = table_client.get_field(
        key_value=breaking_bad_tv_show_record_key_value, field_path='ratings.imdb'
    )
    print(f"Breaking bad imdb rating : {retrieved_breaking_bad_tv_show_imdb_rating}")

    retrieved_hannibal_tv_show_imdb_rating: Optional[Union[int, float]] = table_client.get_field(
        key_value=hannibal_tv_show_record_key_value, field_path='ratings.imdb'
    )
    print(f"Hannibal imdb rating : {retrieved_hannibal_tv_show_imdb_rating}")


```

### Output
```
Retrieved tv shows : {
    'b12': {'name': {'value': 'Breaking Bad', 'fromCache': False}, 'ratings': {'value': {'imdb': 9.4)}, 'fromCache': False}},
    'd52': {'name': {'value': 'Hannibal', 'fromCache': False}, 'ratings': {'value': {'imdb': 8.5}, 'fromCache': False}}
}
TV shows names to keys : {'Breaking Bad': 'b12', 'Hannibal': 'd52'}
Breaking bad imdb rating : {'value': 9.4, 'fromCache': False}
Hannibal imdb rating : {'value': 8.5, 'fromCache': True}
```
        
