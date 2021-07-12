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