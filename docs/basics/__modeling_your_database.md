---
id: modeling_your_database
title: Modeling your database
---


### Introduction :

Everything start with your model.

All data that you will insert or retrieve from your data will need to conform to your model.

Your model is immutable and should not be changed at runtime.

All possible fields of your database will statically be indexed once in the lifecycle of your application, which allows
immediate access to the metadata of any field in your table, no matter if they are nested or how deep they are nested, 
without any performance cost compared to a field at the root of your table.


### Creating your table model class

Create a new class with any name, that inherit from the TableDataModel class.
Add a required field of type str, 

```python
from StructNoSQL import TableDataModel, BaseField

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
```

### 2 - Creating a simple required field
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

```python
from StructNoSQL import TableDataModel, BaseField

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    username = BaseField(field_type=str, required=True)
    age = BaseField(field_type=(int, float, str), required=None)
```


### Adding dictionaries/map's
You can create structured dictionaries, where you can have as many items as you want with different key names, but still
keep the items values structured.

First create a ```MapModel``` that will be the model of each item in your dictionary.
Inside the ```MapModel```` (node the indentation), we define the different fields of the dictionary items the same way
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
    username = BaseField(field_type=str, required=True)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(field_type=int, required=True)
    tokens = BaseField(field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)
```

You can name your ```MapModel``` class any way you want, in our example we keep are creating a dictionary of 
authentication tokens, so we keep the name descriptive with ```AuthTokenModel```. 

You can also create the ```MapModel``` in other files or outside the ```TableDataModel```, unlike what is
showed in the example, our example stay descriptive by creating the model right above its usage.

### Adding dictionaries/map's
```python
from StructNoSQL import TableDataModel, BaseField, MapModel
from typing import Dict

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class AuthTokenModel(MapModel):
        expirationTimestamp = BaseField(field_type=int, required=True)
    tokens = BaseField(field_type=Dict[str, AuthTokenModel], key_name='tokenId', required=False)

```

### Creating self nested models
```python
from typing import Any, Dict
from StructNoSQL import MapModel, BaseField, ActiveSelf

class ParameterModel(MapModel):
    value = BaseField(field_type=Any, required=False)
    childParameters = BaseField(field_type=Dict[str, ActiveSelf], key_name='childParameterKey{i}', max_nested_depth=8, required=False)
parameters = BaseField(field_type=Dict[str, ParameterModel], key_name='parameterKey', required=False)

```