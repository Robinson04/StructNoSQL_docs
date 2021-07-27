---
id: query_multiple_fields
slug: /api/query_multiple_fields
---

**Query multiple fields from potentially multiple records from your primary or any secondary index. 
Has support for filter's and results pagination.**

```python
from StructNoSQL import QueryMetadata

records_values, query_metadata = table_client.query_multiple_fields(
    key_value: str, field_path: str, query_kwargs: Optional[dict] = None,
    index_name: Optional[str] = None,
    exclusive_start_key: Optional[Any] = None,
    pagination_records_limit: Optional[int] = None,
    filter_expression: Optional[Any] = None, 
    data_validation: bool = True
) 
records_values: Optional[Dict[str, Any]]
query_metadata: QueryMetadata
``` 

Query a field and return of tuple of the both the records_values organized in a dictionary (the keys being the primary key
value of each record), and a [query_metadata](../api/QueryMetadata) object with information needed to paginate your query. 

:::tip This operation is paginated
When the number of records you specified in pagination_records_limit have been scanned, or as soon as the data that you
will be returned reached 1MB of size, your query will be paginated into multiple pages.
Refer yourself to [Query pagination](../basics/query_pagination) in order to work with paginated responses.
:::

You can use [paginated_query_multiple_fields](../api/paginated_query_multiple_fields.md) for a managed navigation of 
paginated results with a simple iterable.

## Parameters
| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| index_name | No | str | primary_index name of table | The index\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto.
| key_value | YES | Any | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| getters | YES | Dict[str,&nbsp;[FieldGetter](../api/FieldGetter)] | - | A dictionary with all the fields to retrieve, and the keys that will be used for the output you will receive. |
| exclusive_start_key | NO | dict | None | The key object to start the query from. This is used in paginated queries, it should not be manually created but retrieved from the 'last_evaluated_key' attribute from the [query_metadata](../api/QueryMetadata) of your previous query operation.
| pagination_records_limit | NO | int | None | The numbers of records to scan before paginating the query. If None, the query will execute until all records matching the key_value have been scanned, or when the retrieved fields from the records exceed 1MB.
| filter_expression | NO | Any | None | Take and apply any condition from boto3.dynamodb.conditions. See : https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/dynamodb/conditions.html
| data_validation | NO | bool | True | Whether data validation from your table model should be applied on the retrieved data. 
 
## Availability
| Table | Available |
| ----- | :-------- |
| DynamoDBBasicTable | ✅
| DynamoDBCachingTable | ✅
| ExternalDynamoDBApiBasicTable | ✅
| ExternalDynamoDBApiCachingTable | ✅

## Related pages
- [Query pagination](../basics/query_pagination)
- [QueryMetadata](../api/QueryMetadata)
- [paginated_query_multiple_fields](../api/paginated_query_multiple_fields)

## Example

### Queried record
```json
[
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
  },
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
    "id": "n96",
    "name": "The Walking Dead",
    "primaryType": "Thriller",
    "ratings": {
      "imdb": 8.2,
      "rottentomatoes": null
    }
  },
  {
    "id": "o28",
    "name": "Amazon Lord of the Rings",
    "primaryType": "Fantasy",
    "ratings": {
      "imdb": null,
      "rottentomatoes": null
    }
  },
  {
    "id": "h57",
    "name": "Narcos",
    "primaryType": "Thriller",
    "ratings": {
      "imdb": 8.8,
      "rottentomatoes": null
    }
  },
  {
    "id": "p05",
    "name": "Chernobyl",
    "primaryType": "Thriller",
    "ratings": {
      "imdb": 9.4,
      "rottentomatoes": null
    }
  },
  {
    "id": "m19",
    "name": "The Witcher",
    "primaryType": "Fantasy",
    "ratings": {
      "imdb": 8.2,
      "rottentomatoes": null
    }
  },
  {
    "id": "b45",
    "name": "Dark",
    "primaryType": "Thriller",
    "ratings": {
      "imdb": 8.8,
      "rottentomatoes": null
    }
  }
]
```

### Code
```python
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

```

### Output
```
Here is some thriller tv shows you might enjoy :
{'name': 'Narcos', 'imdb_rating': 8.8} (id: h57)
{'name': 'The Walking Dead', 'imdb_rating': 8.2} (id: n96)
{'name': 'Dark', 'imdb_rating': 8.8} (id: b45)

Here is some thriller tv shows you might enjoy :
{'name': 'Breaking Bad', 'imdb_rating': 9.4} (id: b12)
{'name': 'Hannibal', 'imdb_rating': 8.5} (id: d52)
{'name': 'Chernobyl', 'imdb_rating': 9.4} (id: p05)

No tv shows found in response, you might have hit the end of records.

All tv shows have been retrieved.
```
        
 