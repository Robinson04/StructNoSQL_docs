---
id: query_field
slug: /api/query_field
---

**Query a single field from potentially multiple records from your primary or any secondary index. 
Has support for filter's and results pagination.**

```python
from StructNoSQL import QueryMetadata

records_values, query_metadata = table_client.query_field(
    key_value: str, field_path: str, query_kwargs: Optional[dict] = None,
    index_name: Optional[str] = None,
    exclusive_start_key: Optional[Any] = None,
    pagination_records_limit: Optional[int] = None,
    filter_expression: Optional[Any] = None, 
    data_validation: bool = True
) 
records_values: Optional[dict]
query_metadata: QueryMetadata
``` 

Query a field and return of tuple of the both the records_values organized in a dictionary (the keys being the primary key
value of each record), and a  [query_metadata](../api/QueryMetadata) object with information needed to paginate your query. 

:::tip This operation is paginated
When the number of records you specified in pagination_records_limit have been scanned, or as soon as the data that you
will be returned reached 1MB of size, your query will be paginated into multiple pages.
Refer yourself to [Querying fields](../basics/querying_fields) in order to work with paginated responses.
:::

You can use [paginated_query_field](../api/paginated_query_field.md) for a managed navigation of 
paginated results with a simple iterable.
 
## Parameters
| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| index_name | No | str | primary_index name of table | The index\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto.
| key_value | YES | Any | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| field_path | YES | str | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| query_kwargs | NO | dict | None | Used to pass data to populate a field_path that contains keys. See example below :
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
- [Querying fields](../basics/querying_fields)
- [QueryMetadata](../api/QueryMetadata)
- [paginated_query_field](../api/paginated_query_field)

## Example

### Queried record
```json
[
  {
    "id": "c30",
    "name": "Game of Thrones",
    "primaryType": "Fantasy"
  },
  {
    "id": "d52",
    "name": "Hannibal",
    "primaryType": "Thriller"
  },
  {
    "id": "b12",
    "name": "Breaking Bad",
    "primaryType": "Thriller"
  },
  {
    "id": "n96",
    "name": "The Walking Dead",
    "primaryType": "Thriller"
  },
  {
    "id": "o28",
    "name": "Amazon Lord of the Rings",
    "primaryType": "Fantasy"
  },
  {
    "id": "h57",
    "name": "Narcos",
    "primaryType": "Thriller"
  },
  {
    "id": "p05",
    "name": "Chernobyl",
    "primaryType": "Thriller"
  },
  {
    "id": "m19",
    "name": "The Witcher",
    "primaryType": "Fantasy"
  },
  {
    "id": "b45",
    "name": "Dark",
    "primaryType": "Thriller"
  }
]
```

### Code
```python
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

```

### Output
```
Here is 3 thriller tv shows i think you will enjoy :
Narcos (id: h57)
The Walking Dead (id: n96)
Dark (id: b45)

Here is 3 other thriller tv shows :
Breaking Bad (id: b12)
Hannibal (id: d52)
Chernobyl (id: p05)

I have some remaining movies to show you
```
        
 