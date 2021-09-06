---
id: modeling_your_database
title: Modeling your database
---


### Introduction

Everything start with your model.

All data that you will insert or retrieve from your data will need to conform to your model.

Your model is immutable and should not be changed at runtime.

All possible fields of your database will statically be indexed once in the lifecycle of your application, which allows
immediate access to the metadata of any field in your table, no matter if they are nested or how deep they are nested, 
without any performance cost compared to a field at the root of your table.


### 1 - Creating your table model class

Create a new class with any name, that inherit from the ```TableDataModel``` class.

Add a first field. This is the field that will be used as the primary key value for your records.
Your table model is not connected to your table client, make sure to properly set this field accordingly to what you 
configured in your table client.

The name of this primary key value field should be the same as the ```hash_key_name``` of the ```PrimaryIndex``` of your 
defined in your table_client. The ```field_type``` should be the same as the ```hash_key_variable_python_type``` of your 
```PrimaryIndex``` (hence, either ```str``` or ```int```). 

Set the field as required by passing a value of ```True``` to the ```required``` parameter.

```python
from StructNoSQL import TableDataModel, BaseField

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
```

### 2 - Root required field's
The same way you defined as required the field used as the primary key value of your records (in our example, ```userId```),
you can create other required fields by setting the ```required``` parameter of your field to ```True```.

Our ```username``` required field is at the root of the record, which means that when creating a record, the 
```username``` field will need to be present, otherwise the record creation will fail. This also means that 
```username``` cannot be removed or deleted, but can be updated.  

```python
from StructNoSQL import TableDataModel, BaseField

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=True)
```

### 3 - Fields with multiple allowed types
You can allow multiple types in a field, by creating a tuple of types, by wrapping the multiple fields with parenthesis.
```python
from StructNoSQL import TableDataModel, BaseField

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    age = BaseField(field_type=(int, float, str), required=True)
```

### 4 - Non required root fields
You can set a field as non required. If the field is at the root of your record, you will be able to create a record 
without specifying values for your non-required fields.
In addition to the ```field_type``` you specified, a non-required field will also accept a ```None``` value as a valid 
value.

```python
from StructNoSQL import TableDataModel, BaseField

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    nextReminderTimestamp = BaseField(field_type=int, required=False)
```

Use non required fields both for non-crucial fields, and for fields you have added after the first deployment of your
database. Otherwise, you might end-up with old records that are missing some fields that are not required, and will not
be considered as valid by StructNoSQL.

### 5 - Allowing any value in a field

To allow any value in a field, import ```Any``` from the ```typing``` module (which is pre-installed with Python), and
use it as the field_type of your field.

```python
from StructNoSQL import TableDataModel, BaseField
from typing import Any

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    requiredUserStatus = BaseField(field_type=Any, required=True)
    optionalMetadata = BaseField(field_type=Any, required=False)
```

:::important Required fields that accept any value still need to be specified
Even tough a field accepting any value, will consider a value of ```None``` to be valid, the attribute will
still need to be specified. 
In our example above, if you tried to create a new record without specifying the ```requiredUserStatus``` attribute, the 
record creation would fail. 
Whereas ```optionalMetadata``` also can accept any value, but since it is not a required field, not specifying it will 
not cause a record creation to fails.
:::

### 6 - Structured map's
You can create ```MapModel``'s allowing to group multiple fields inside a dictionary.

First create a new class that inherit from ```MapModel```. You can name the class however you want, in our example we
use ```MetadataModel``` which is pretty descriptive.
Inside this class, define the various fields of your model, similarly to how we were defining the fields of your 
```TableDataModel```. 
Finally, create a new field (for example ```metadata```) and set its field_type to the ```MapModel``` class you created.

In our example, metadata is not required, but if it was the case, the required fields of the ```MetadataModel``` would
also be required. Since metadata is at the root of the table data model, this means that if metadata would be required,
any record would need the metadata field to be a dictionary that at least contain the ```accountCreationTimestamp``` attribute.

```python
from StructNoSQL import TableDataModel, BaseField, MapModel

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class MetadataModel(MapModel):
        accountCreationTimestamp = BaseField(field_type=int, required=True)
        lastConnectionTimestamp = BaseField(field_type=int, required=False)
    metadata = BaseField(field_type=MetadataModel, required=False)
```

Note that in our example we create the ```MetadataModel``` class inside the scope of the ```UsersTableModel``` to keep
the code clearer. But nothing stops you to create your ```MapModel```'s outside of the scope of your existing table data
model, or even in totally different files, and then being able to use them as ```field_type``` for one of your field.

You can now target with a field_path any field that is inside of your ```MapModel````.

Example usage :
```python
from typing import Optional

account_creation_timestamp_from_metadata: Optional[int] = table_client.get_field(
    field_path='metadata.accountCreationTimestamp'
)
```

### 7 - Structured dictionaries
You can create structured dictionaries, where you can have as many items as you want with different key names, but still
keep the items values structured.

First create a ```MapModel``` that will be the model of each item in your dictionary.
Inside the ```MapModel``` (note the indentation), we define the different fields of the dictionary items the same way
we did previously.

Note that our ```expirationTimestamp``` field is required. When 

Then, create the actual dictionary field (the ```tokens``` field). To define it as a dictionary, import ```Dict``` from
the ```typing``` module (no need to download it, ```typing``` is part of the standard Python modules already installed).
Define the ```field_type``` as dictionary, with the first type being the type of the keys that you want (you can use
```str```, ```int``` or ```float``` as key types), then pass your previously created ```MapModel``` as the second 
argument, which will be the model of your data.

Then, define the ```key_name``` of your field. It is a special parameter that can only be used on a field with a 
```Dict``` field type, and will be used to target your dictionary items with field paths.

When first launching your application and instantiating your table client for the first time, the model of your 
database will be indexed, and kept statically in the memory of your application into a flattened dictionary that will 
act a switch. When targeting a field, you will specify its exact field path, which will looked for in the fields switch,
without any performances cost, no matter the location of the field.

Since you can create as many items with totally different keys in a dictionary, you will not directly specify the key
of the dictionary item your want to target. You will specify its key name in the field path, and then pass a variable
that will populate the key name.

Example usage :
```python
from typing import Optional

retrieved_expiration_timestamp: Optional[int] = table_client.get_field(
    field_path='tokens.{{tokenId}}.expirationTimestamp',
    query_kwargs={'tokenId': "exampleTokenIdentifier"}
)
```

StructNoSQL index all the possible fields of your table to a switch, which then allows you to target any field,
no matter its location without performances costs. 


```python
from StructNoSQL import TableDataModel, BaseField, MapModel
from typing import Dict

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(field_type=int, required=True)
    tokens = BaseField(field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)
```

You can name your ```MapModel``` class any way you want, in our example we keep are creating a dictionary of 
authentication tokens, so we keep the name descriptive with ```AuthTokenModel```. 

You can also create the ```MapModel``` in other files or outside the ```TableDataModel```, unlike what is
showed in the example, our example stay descriptive by creating the model right above its usage.


### 8 - Non required nested fields
Similarly to [non required root fields](../basics/modeling_your_database#4---non-required-root-fields), you can also
create non-required fields inside nested ```MapModel```'s.
When creating/updating/retrieving items from a dictionary or a list, each item will be validated individually. If you
try to retrieve or update multiple items at the same time, if one or more of them are invalid, they will be silently
discarded (a message will be logged to indicate the reason why the item is discarded), and the remaining items will be 
sent to your database or returned to you. If none of them are valid, either no operation will be sent to the database, 
or you will be returned a ```None``` value.

You will also be able to delete or remove nested non-required fields.

```python
from StructNoSQL import TableDataModel, BaseField, MapModel
from typing import Dict

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(field_type=int, required=True)
        tokenMetadata = BaseField(field_type=dict, required=False)
    tokens = BaseField(field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)
```


### 9 - Nested structured dictionary fields
You can create keep nesting fields, dictionary or list's inside a structured list, until you reach the maximum 32 depth 
limit imposed by DynamoDB (see [The depth limit](../basics/recursive_nesting#the-depth-limit)).

```python
from StructNoSQL import TableDataModel, BaseField, MapModel
from typing import Dict

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(field_type=int, required=True)
        class PermissionMetadataModel(MapModel):
            permissionGrantedBy = BaseField(field_type=str, required=True)
            permissionExpirationTimestamp = BaseField(field_type=int, required=False)
        tokenPermissions = BaseField(field_type=Dict[str, PermissionMetadataModel], key_name='permissionKey', required=False)
    tokens = BaseField(field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)
```

Example usage :
```python
from typing import Optional

token_write_permission_metadata: Optional[dict] = table_client.get_field(
    field_path='tokens.{{tokenId}}.tokenPermissions.{{permissionKey}}',
    query_kwargs={'tokenId': "exampleTokenId", 'permissionKey': "write"}
)
```

:::info A structured dictionary has a depth of 2 items
Even tough you only define one field, a structured dictionary is actually composed of two dictionaries. The first one
holding all of your items, and the second depth of dictionary being your items dictionaries holding the attributes of
your items.

This means that two nested structured dictionaries have a depth of 4, and four nested of them have depth of 8. The
maximum depth limit imposed by StructNoSQL is 32 (see [The depth limit](../basics/recursive_nesting#the-depth-limit)). 

It is unlikely you will ever reach this limit, but if it's the case, it cannot be increased by StructNoSQL or by 
DynamoDB. Thus, you should consider restructuring your data, maybe by flattening it as shown in 
[NoSQL best practices/Flattening data](../nosql-best-practices/flattening-data)
:::

### 10 - Primitive dictionary fields
You can also create dictionary fields that accept primitive values that are not structured. You can use any primitive type
like ```int```, ```float```, ```dict```, ```list```, etc. You can also allow multiple types at the same time by wrapping 
them with parenthesis.

```python
from StructNoSQL import TableDataModel, BaseField
from typing import Dict

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    orderedLogMessages = BaseField(field_type=Dict[str, (str, dict)], key_name='logId', required=False)
```

:::info Unstructured data cannot be navigated into
Even if you define the item type of your list to be a ```dict``` or ```list```, since it is unstructured, you will not
be able to navigate into or select specific attributes to retrieve/update/delete inside your list items like you
can do with a structured list field as shown above. You will only be able to target the entire dict or list value.
:::

Example usage :
```python
from typing import Optional, Union

third_log_message: Optional[Union[str, dict]] = table_client.get_field(
    field_path='orderedLogMessages.{{logId}}',
    query_kwargs={'logIndex': "exampleLogId"}
)
```


### 11 - Unvalidated dictionary fields
To create a list that can accept any values, either create a field with a ```field_type``` of ```dict``` or of 
```Dict[Any]``` (import both ```Dict``` and ```Any``` from the typing module).

Similarly to a primitive dict field showcased in 
[Primitive dictionary fields](../basics/modeling_your_database#10--primitive-dictionary-fields), the data will be
unstructured, you will not be able to navigate into your dict items.

```python
from StructNoSQL import TableDataModel, BaseField
from typing import Dict, Any

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    primaryOrderedLogMessages = BaseField(field_type=dict, key_name='logId', required=False)
    secondaryOrderedLogMessages = BaseField(field_type=Dict[str, Any], key_name='logId', required=False)
    # Both primary and secondary orderedLogMessages fields are equivalent
```

Example usage :
```python
from typing import Optional, Any

third_log_message: Optional[Any] = table_client.get_field(
    field_path='primaryOrderedLogMessages.{{logId}}',
    query_kwargs={'logId': "exampleLogId"}
)
```


### 11 - Structured list fields
You can create list where specific 
```python
from StructNoSQL import TableDataModel, BaseField, MapModel
from typing import List

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class FriendModel(MapModel):
        friendId = BaseField(field_type=str, required=True)
        friendsSinceTimestamp = BaseField(field_type=int, required=True)
    orderedFriends = BaseField(field_type=List[FriendModel], key_name='friendIndex', required=False)
```

Example usage :
```python
from typing import Optional

third_friend_id: Optional[str] = table_client.get_field(
    field_path='orderedFriends.{{friendIndex}}.friendId',
    query_kwargs={'friendIndex': 3}
)
```

### 12 - Nested structured list fields
You can create keep nesting fields, dictionary or list's inside a structured list, until you reach the maximum 32 depth 
limit imposed by DynamoDB (see [The depth limit](../basics/recursive_nesting#the-depth-limit)).

```python
from StructNoSQL import TableDataModel, BaseField, MapModel
from typing import List

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class FriendModel(MapModel):
        friendId = BaseField(field_type=str, required=True)
        friendsSinceTimestamp = BaseField(field_type=int, required=True)
        class SharedInterestModel(MapModel):
            friendId = BaseField(field_type=str, required=True)
        sharedFriends = BaseField(field_type=List[SharedInterestModel], key_name='sharedFriendIndex', required=False)
    orderedFriends = BaseField(field_type=List[FriendModel], key_name='friendIndex', required=False)
```

:::warning Avoid overlapping key names
Make sure properly define unique key_name's in your fields, to overlapping key names in the same possible field path.
For example, if you have a 'friends' field, that is of type ```List[FriendModel]``` with a key_name of 'friendIndex', 
then inside ```FriendModel```, you have a field name 'sharedFriends' that is a list that also use 'friendIndex' as a 
key_name. This would cause the 'friendIndex' key name to overlap if you tried to target the sharedFriend field. When 
populating your key names with query_kwargs, you would end up not being able to define different values for both keys. 
If this happens, do not worry, the key_name's of fields are not stored in your database, and can be changed at any time 
without overhead.
:::

Example usage :
```python
from typing import Optional

second_shared_friend_id_of_third_friend: Optional[dict] = table_client.get_field(
    field_path='orderedFriends.{{friendIndex}}.sharedFriends.{{sharedFriendIndex}}',
    query_kwargs={'friendIndex': 3, 'sharedFriends': 2}
)
```

### 13 - Primitive list fields
You can also create list fields that accept primitive values that are not structured. You can use any primitive type
like ```int```, ```float```, ```dict```, ```list```, etc. You can also allow multiple types at the same time by wrapping 
them with parenthesis.

```python
from StructNoSQL import TableDataModel, BaseField
from typing import List

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    orderedLogMessages = BaseField(field_type=List[(str, dict)], key_name='logIndex', required=False)
```

:::info Unstructured data cannot be navigated into
Even if you define the item type of your list to be a ```dict``` or ```list```, since it is unstructured, you will not
be able to navigate into or select specific attributes to retrieve/update/delete inside your list items like you
can do with a structured list field as shown above. You will only be able to target the entire dict or list value.
:::

Example usage :
```python
from typing import Optional, Union

third_log_message: Optional[Union[str, dict]] = table_client.get_field(
    field_path='orderedLogMessages.{{logIndex}}',
    query_kwargs={'logIndex': 3}
)
```

### 14 - Unvalidated list fields
To create a list that can accept any values, either create a field with a ```field_type``` of ```list``` or of 
```List[Any]``` (import both ```List``` and ```Any``` from the typing module).

Similarly to a primitive list field showcased in 
[Primitive list fields](../basics/modeling_your_database#8--primitive-list-fields), the data will be
unstructured, you will not be able to navigate into your list items.

```python
from StructNoSQL import TableDataModel, BaseField
from typing import List, Any

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    primaryOrderedLogMessages = BaseField(field_type=list, key_name='logIndex', required=False)
    secondaryOrderedLogMessages = BaseField(field_type=List[Any], key_name='logIndex', required=False)
    # Both primary and secondary orderedLogMessages fields are equivalent
```

Example usage :
```python
from typing import Optional, Any

third_log_message: Optional[Any] = table_client.get_field(
    field_path='primaryOrderedLogMessages.{{logIndex}}',
    query_kwargs={'logIndex': 3}
)
```

### 15 - Recursive nesting
You can recursively nest a ```MapModel``` inside itself by using the ```ActiveSelf```.
You can use it both by itself to create a recursive map, or inside a ```List``` or ```Dict```.
This is a delicate feature, read more about how to use it here : [Recursive nesting](../basics/recursive_nesting)

```python
from StructNoSQL import TableDataModel, MapModel, BaseField, ActiveSelf
from typing import Any, Dict

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class ParameterModel(MapModel):
        value = BaseField(field_type=Any, required=False)
        childParameter = BaseField(field_type=ActiveSelf, required=False)
        childrenParameters = BaseField(field_type=Dict[str, ActiveSelf], key_name='childParameterKey{i}', max_nested_depth=8, required=False)
    parameters = BaseField(field_type=Dict[str, ParameterModel], key_name='parameterKey', required=False)
```