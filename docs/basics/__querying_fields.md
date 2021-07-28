---
id: querying_fields
slug: /basics/querying_fields
title: Querying fields
---

The 'get' operations can retrieve fields from a record when you select it with its primary key value. To retrieve 
records based on secondary indexes, you need to query your records as showed in the 
[Query fields](../basics/query_fields.md) page.

You have multiple operations at your disposition :

- [query_field](../api/query_field.md)
- [query_multiple_fields](../api/query_multiple_fields.md)
- [paginated_query_field](../api/paginated_query_field.md)
- [paginated_query_multiple_fields](../api/paginated_query_multiple_fields.md)


### Creating the table for our example
```python
import json
from typing import Dict
from StructNoSQL import TableDataModel, BaseField, MapModel, \
    DynamoDBBasicTable, PrimaryIndex, GlobalSecondaryIndex

class UsersTableModel(TableDataModel):
    accountId = BaseField(field_type=str, required=True)
    profession = BaseField(field_type=str, required=True)
    age = BaseField(field_type=int, required=True)
    username = BaseField(field_type=str, required=False)
    class FriendItemModel(MapModel):
        name = BaseField(field_type=str, required=True)
        relationship = BaseField(field_type=str, required=False)
        achievements = BaseField(field_type=Dict[str, bool], key_name='achievementKeyName', required=False)
    friends = BaseField(field_type=Dict[str, FriendItemModel], key_name='friendId', required=False)
    class MetadataModel(MapModel):
        lastLoginTimestamp = BaseField(field_type=int, required=False)
    metadata = BaseField(field_type=MetadataModel, required=False)

class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(
            hash_key_name='userId', 
            hash_key_variable_python_type=str
        )
        super().__init__(
            table_name="my-first-table", region_name="eu-west-2", 
            primary_index=primary_index, auto_create_table=True,
            data_model=UsersTableModel, global_secondary_indexes=[
                GlobalSecondaryIndex(
                    hash_key_name='age',
                    hash_key_variable_python_type=int,
                    projection_type='ALL'
                ),
                GlobalSecondaryIndex(
                    hash_key_name='profession',
                    hash_key_variable_python_type=str,
                    projection_type='ALL'
                )
            ]
        )

table_client = UsersTable()

with open("record.json", 'r') as file:
    source_record_data: dict = json.load(fp=file)
    put_record_success: bool = table_client.put_record(record_dict_data=source_record_data)
    if put_record_success is not True:
        print("Error with put_record")
```


### 1 - Querying a single field value from a secondary index
You can use [query_field](../api/query_field) to retrieve a single field value from multiple records.

Specify the index you want to query (for example, profession). You can also specify your primary index (for example, 
userId), but DynamoDB enforces uniqueness on primary index values, which means that a query on the primary index will
never return more than one record item, it is more efficient to use the 'get operations' detailed in 
[Retrieving fields](../basics/retrieving_fields). The only exception would be if you wanted to add filter expression
to a request on the primary index, as showcased in example 1.

Similarly to the [get_field](../api/get_field) operation, you must specify the ```key_value``` of the records you want
to query. And ```field_path``` to select the field you want to retrieve in each record.
```python
from typing import Optional
from StructNoSQL import QueryMetadata

retrieved_records_value, query_metadata = table_client.query_field(
    index_name='profession', key_value='designer', field_path='username'
)
retrieved_records_value: Optional[dict]
query_metadata: QueryMetadata
for record_primary_key_value, record_retrieved_username_value in retrieved_records_value.items():
    print(f"username: {record_retrieved_username_value} & id: {record_primary_key_value}")
```
```retrieved_records_value``` will contain a dictionary where the keys will be the primary key values of each record
queried, and the values will be the matching field you requested for each record.
```query_metadata``` old information about the state of the query, that will be required if you need to paginate your
query result into multiple pages.

Note that when the combined size of the attributes you are retrieving from each of your queried records reach 1MB of
size, or when the number of scanned records reach the ```pagination_records_limit``` parameter (if you specified it),
your query operation will automatically be split into multiple pages. If you know for a fact you will have only
a few records, you can use ```query_field``` without worrying about pagination, but it would be better to always treat
results from query operations as potentially paginated, as showcased in the examples below.


### 2 - Querying a single field value from a secondary index and navigate trough pages managed
The easiest way to perform a paginated query for the retrieval of single field is to use the 
[paginated_query_field](../api/paginated_query_field).

Specify 

You will be returned a ```Generator```, it is similar to an iterable, you can loop over it like a list, but does not has
a pre-determined length, and will create the items as you iterate over him (in our case, creating the items is sending a
database request to get the next page of query results).

Specify the primary key value of the records you want to retrieve the field from with the ```key_value``` parameter.
Specify the field you want to retrieve with ```field_path```.
```python
from typing import Generator, Tuple, Optional
from StructNoSQL import QueryMetadata

records_paginator: Generator[Tuple[Optional[dict], QueryMetadata], None, None] = (
    users_table.paginated_query_field(
        index_name='profession', key_value='designer', 
        field_path='username', pagination_records_limit=10
    )
)
for retrieved_records_value, query_metadata in records_paginator:
    if retrieved_records_value is not None:
        print(f"Here is 10 or less designers :")
        for record_primary_key_value, record_retrieved_username_value in retrieved_records_value.items():
            print(f"username: {record_retrieved_username_value} & id: {record_primary_key_value}")
print("All the designers have been queried.")
```
If no value has been found or if it did not pass the data validation, ```retrieved_value``` will be None.
The typing with ```Optional[str]``` is not required.

### 2 - Querying a single field value from a secondary index and navigate trough maximum amounts of pages managed

Since the requests are being sent as you iterate over the ```records_paginator```, you can break out of the 
loop at any time, which will stop sending requests for the next pages of query results.

For example, if you want to define a maximum amount of pages to iterate trough, you can keep track of the page index 
(for example, with ```enumerate```), and break out of the records_paginator loop when you have reached your maximum 
amount of pages.

Just make sure to break out of the loop at the end of it, after having used the query page you retrieved. Otherwise,
if you were breaking at the start of the loop, for example as soon as you reach the sixth page, this sixth page would 
have been retrieved from the database for nothing. Instead, you could break at the end of the loop, of the fifth page.

```python
from typing import Generator, Tuple, Optional
from StructNoSQL import QueryMetadata

records_paginator: Generator[Tuple[Optional[dict], QueryMetadata], None, None] = (
    users_table.paginated_query_field(
        index_name='profession', key_value='designer', 
        field_path='username', pagination_records_limit=10
    )
)
for i_page, page_container in enumerate(records_paginator):
    retrieved_records_value, query_metadata = page_container
    if retrieved_records_value is not None:
        print(f"Here is 10 or less designers :")
        for record_primary_key_value, record_retrieved_username_value in retrieved_records_value.items():
            print(f"username: {record_retrieved_username_value} & id: {record_primary_key_value}")
            
    # The i_page created with the enumerate function always 
    # start at zero, so i_page 4 is actually the fifth page.
    if i_page >= 4:
        break
print("Ether 50 (5*10) or all the designers have been queried.")
```

### 3 - Querying a single field value from a secondary index and navigate trough pages manually
Instead of using the [paginated_query_field](../api/paginated_query_field) you can handle pagination of your requests
manually with paginated_query_field.

Specify the index you want to query. You can etheir use a global secondary index defined in your table, or, by default
if not specified, the primary index of your table. Since the primary key values in DynamoDB are unique, there is not a
lot of uses for using query operations on the primary index opposed to the 'get operations' 
[Retrieving fields](../basics/retrieving_fields), unless if you want to specify some filter condition, as showed in 
example 10.

Like a [get_field](../api/get_field) operation, define the key_value where all the records with this , and the 
field_path of the field you want to retrieve.

Optionally, you can set ```pagination_records_limit``` to define a maximum number of records to be scanned before the 
current page of your query ends and a response is returned. If not specified, the page will end if all the records
matching the key_value for the index_name you specified as been scanned, or until the combined size of records 
attributes you requested reach 1MB of size. Otherwise, the same rules applies, with the additional pagination_records_limit.

The navigation between paginated data will be done using the ```exclusive_start_key``` parameter. Notice that the
```query_field``` returns both ```retrieved_records_value``` and ```query_metadata```. The query_metadata contains 4
attributes. The ```count``` attribute, representing how much records have been scanned in the current page of the query
(if you have set some filter conditions, the scanned count can be bigger than the number of records items being 
returned). The ```has_reached_end``` attribute, wether all the records matching the specified key_value and index_name
have been scanned, and you should end your query. Finally, the ```last_evaluated_key``` attribute, a dictionary
containing informations about the last scanned record in your page, that can then be used as an 
```exclusive_start_key``` to start a new page where you left off the last one, resulting in a progressive navigation
trough paginated query results.
If ```exclusive_start_key``` is not defined or set to None, the page will start at the beginning of your records.

```python
from typing import Optional
from StructNoSQL import QueryMetadata

last_evaluated_key: Optional[dict] = None
for i in range(5):
    retrieved_records_value, query_metadata = table_client.query_field(
        index_name='profession', key_value='designer', field_path='username', 
        pagination_records_limit=10, exclusive_start_key=last_evaluated_key
    )
    retrieved_records_value: Optional[dict]
    query_metadata: QueryMetadata

    if query_metadata.has_reached_end is True:
        break
    last_evaluated_key = query_metadata.last_evaluated_key
    print(f"Here is 10 or less designers :")
    for record_primary_key_value, record_retrieved_username_value in retrieved_records_value.items():
        print(f"username: {record_retrieved_username_value} & id: {record_primary_key_value}")
print("Ether 50 (5*10) or all the designers have been queried.")
```
If no value has been found or if it did not pass the data validation, ```retrieved_value``` will be None.
The typing with ```Optional[str]``` is not required.

### 2 - Querying a single field value without data validation from a secondary index
{{file::docs_parts/reason_for_disabling_data_validation.md::}}
```python
from typing import Dict, Optional, Any

retrieved_records_value: Dict[str, Optional[Any]] = table_client.query_field(
    key_value='x42', field_path='username', data_validation=False
)
```
Notice that in our ```get_field``` example, we typed the retrieved_value with ```Optional[str]``` where we assumed that
if the value is not None (with ```Optional```), it will be a ```str```, as per the table model that would only return a 
```str``` as a valid value. Now, since the data_validation is returned, our retrieved value could be anything, so we
type it as ```Optional[Any]```. Note that typing Python code is strictly optional and does not changes anything during
the execution of your code, it is only there to make your code clearer and for your IDE to give quality warnings.


### 3 - Querying multiple fields values with a multi-selector
If you need to retrieve multiple fields that share the same parent path, you can use a multi-selector.
Wrap the multiple fields names you want to retrieve inside parenthesis. This will be similar to using the 
[get_multiple_fiends](../api/get_multiple_fields.md) operation, where the multiple fields will be retrieved with a
single database operation. You will be returned a dictionary with the keys will be all the fields names you requested,
and their retrieved values if they were found.
```python
from typing import Dict, Optional, Any

retrieved_values: Dict[str, Optional[Any]] = table_client.get_field(
    key_value='x42', field_path='(username, friends)'
)
retrieved_username_value: Optional[str] = retrieved_values['username']
retrieved_friends_value: Optional[dict] = retrieved_values['friends']
```
{{template::{
    'filepath': 'docs_parts/templates/multi_selectors_template.md', 
    'variable_name': "retrieved_values", 'individual_target_type_name': "field",
    'default_value': "None", 'attempted_operation_explanation': "tried to retrieve"
}::}}


### 4 - Querying multiple nested fields values with a multi-selector
{{file::docs_parts/you_can_use_multi_selectors_with_nested_fields.md::}}
```python
from typing import Dict, Optional, Any

retrieved_values: Dict[str, Optional[Any]] = table_client.get_field(
    key_value='x42', field_path='friends.{{friendId}}.(name, relationship)',
    query_kwargs={'friendId': 'f42'}
)
retrieved_friend_name_value: Optional[str] = retrieved_values['name']
retrieved_friend_relationship_value: Optional[str] = retrieved_values['relationship']
```
If you need to retrieve fields from totally different places, use [get_multiple_fields](../api/get_multiple_fields)
showcased in the examples below.


### 5 - Querying multiple fields values with query_multiple_fields
You can use [get_multiple_fields](../api/get_multiple_fields) to retrieve multiple fields at once from the same 
record with a single database operation.
Like update_field, you select the record you want to update with its primary key value passed in the ```key_value``` 
parameter.
Specify the different fields you want to retrieved by passing a dictionary of [FieldGetter](../api/FieldGetter).
Similarly to get_field, each [FieldGetter](../api/FieldGetter) requires the field_path parameter, and has an optional 
query_kwargs parameter.
```python
from typing import Dict, Optional, Any
from StructNoSQL import FieldGetter

retrieved_values: Dict[str, Optional[Any]] = table_client.get_multiple_fields(
    key_value='x42', getters={
        'username': FieldGetter(field_path='username'),
        'friend_relationship': FieldGetter(
            field_path='friends.{{friendId}}.relationship', 
            query_kwargs={'friendId': 'f42'}, 
        ),
        'metadata_lastLoginTimestamp': FieldGetter(
            field_path='metadata.lastLoginTimestamp', 
        )
    }
)
retrieved_username: Optional[str] = retrieved_values['username']
retrieved_friend_relationship: Optional[str] = retrieved_values['friend_relationship']
retrieved_last_login_timestamp: Optional[int] = retrieved_values['metadata_lastLoginTimestamp']
```
{{template::{
    'filepath': 'docs_parts/templates/multi_selectors_template.md',
    'variable_name': "retrieved_values", 'individual_target_type_name': "field",
    'default_value': "None", 'attempted_operation_explanation': "tried to retrieve"
}::}}


### 6 - Querying multiple fields values with query_multiple_fields without data validation
{{file::docs_parts/reason_for_disabling_data_validation.md::}}
```python
from typing import Dict, Optional, Any
from StructNoSQL import FieldGetter

retrieved_values: Dict[str, Optional[Any]] = table_client.get_multiple_fields(
    key_value='x42', getters={
        'username': FieldGetter(field_path='username'),
        'friend_relationship': FieldGetter(
            field_path='friends.{{friendId}}.relationship', 
            query_kwargs={'friendId': 'f42'}, 
        ),
        'metadata_lastLoginTimestamp': FieldGetter(
            field_path='metadata.lastLoginTimestamp', 
        )
    }, data_validation=False  # <-- disable data_validation
)
retrieved_username: Optional[Any] = retrieved_values['username']
retrieved_friend_relationship: Optional[Any] = retrieved_values['friend_relationship']
retrieved_last_login_timestamp: Optional[Any] = retrieved_values['metadata_lastLoginTimestamp']
```

#### 10 - Querying a single field with a simple filter condition


#### 11 - Querying a single field with a complex filter condition