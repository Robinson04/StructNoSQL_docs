---
id: paginated_query_field
slug: /api/paginated_query_field
---

**Wrapper on the [query_field](../api/query_field.md) operation, that allows to easily perform 
paginated operation with an iterable instead of manually managing the pagination.**

```python
from StructNoSQL import QueryMetadata
from typing import Generator, Tuple, Optional

records_paginator: Generator[Tuple[Optional[dict], QueryMetadata], None, None] = (
    table_client.paginated_query_field(
        index_name=Optional[str], key_value=Any,
        field_path=str, pagination_records_limit=Optional[int],
        pagination_records_limit=Optional[int] = None,
        exclusive_start_key: Optional[Any] = None,
        filter_expression=Optional[Any] = None,
        data_validation: bool = True
    )
)
for records_items, query_metadata in records_paginator:
    if records_items is not None:
        for record_primary_key_value, record_item_data in records_items.items():
            print(record_primary_key_value)
            print(record_item_data)  # do stuff
```

:::info The query request's are being send as you call the records_paginator
Feel free to break out of the loop of the records_paginator, since the query requests are sent progressively only as you 
iterate over the records_paginator. This means that you call that you cannot calculate the length of records_paginator
in order to know the number of records page to except.
:::

:::tip You can also use manual pagination
Notice that the operation has support for the exclusive_start_key, and each item of the records_paginator is a tuple
containing both the records_items and the query_metadata. This allows you to start you records_paginator at a specific
point to resume from a previous query operation, and you can save the last_evaluated_key of the query_metadata's to
continue your query operation later as detailed in [Query pagination](../basics/query_pagination)
:::

## Parameters
| Property&nbsp;name | Required | Accepted&nbsp;types | Default | Description |
| ------------------ | :------: | :-----------------: | :-----: | :---------- |
| index_name | No | str | primary_index name of table | The index\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto.
| key_value | YES | Any | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| field_path | YES | str | - | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md)
| query_kwargs | NO | dict | None | Used to pass data to populate a field_path that contains keys. See example below :
| exclusive_start_key | NO | dict | None | The key object to start the query from. This is used in paginated queries, it should not be manually created but retrieved from the 'last_evaluated_key' attribute from the [query_metadata](../api/QueryMetadata) of your previous query operation.
| pagination_records_limit | NO | int | None | The numbers of records to scan before paginating the query. If None, the query will execute until all records matching the key_value have been scanned, or when the retrieved fields from the records exceed 1MB.
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
- [query_field](../api/query_field)

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
from typing import Optional, List, Generator, Tuple


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


records_paginator: Generator[Tuple[Optional[dict], QueryMetadata], None, None] = (
    table_client.paginated_query_field(
        index_name='primaryType', key_value='Thriller',
        field_path='name', pagination_records_limit=3
    )
)
for records_items, query_metadata in records_paginator:
    if records_items is not None:
        if len(records_items) > 0:
            print("\nHere is some thriller tv shows you might enjoy :")
            for record_primary_key_value, record_movie_name in records_items.items():
                print(f"{record_movie_name} (id: {record_primary_key_value})")
        else:
            print("\nNo tv shows found in response, you might have hit the end of records.")
print("\nAll tv shows have been retrieved.")

```

### Output
```
Here is some thriller tv shows you might enjoy :
Narcos (id: h57)
The Walking Dead (id: n96)
Dark (id: b45)

Here is some thriller tv shows you might enjoy :
Breaking Bad (id: b12)
Hannibal (id: d52)
Chernobyl (id: p05)

No tv shows found in response, you might have hit the end of records.

All tv shows have been retrieved.
```
        
 