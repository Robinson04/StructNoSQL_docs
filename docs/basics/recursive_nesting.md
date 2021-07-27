---
id: recursive_nesting
title: Recursive nesting
---

This is a delicate functionality. Do not try to do recursive nesting if this is your first time using StructNoSQL.

### Step 1 : Creating your field with the ActiveSelf object

```python
class ParameterModel(MapModel):
    childParameters = BaseField(
        name='childParameters', 
        field_type=Dict[str, ActiveSelf]
    )
```

Import the ```ActiveSelf``` object from StructNoSQL, then from inside a MapModel class, use it to define the field_type 
attribute of a ```BaseField```.

```python
from StructNoSQL import TableDataModel, MapModel, BaseField, ActiveSelf
from typing import Dict

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class ParameterModel(MapModel):
        childParameters = BaseField(field_type=Dict[str, ActiveSelf], required=False)
    parameters = BaseField(field_type=Dict[str, ParameterModel], key_name='parameterKey', required=False)
```

:::tip Can be used in complex field_type's
All three usages below of the ActiveSelf object are valid.
```python
from typing import List, Dict
from StructNoSQL import BaseField, ActiveSelf

childParameters = BaseField(field_type=ActiveSelf)
childParameters = BaseField(field_type=List[ActiveSelf])
childParameters = BaseField(field_type=Dict[str, ActiveSelf])
```
:::

:::warning Usage outside a Map Model
You cannot use the ActiveSelf object outside a ```MapModel```. 

For example, you could not use it in a field that is at the root of your table.
:::

### Step 2 : Adding the {i} placeholder

```python
childParameters = BaseField(field_type=Dict[str, ActiveSelf], key_name='childParameterKey{i}')
```
As soon as you use the ActiveSelf object in a field of type List or Dict, you will need to specify a key_name attribute 
if you did not yet specify one, and you will need to add `{i}` anywhere inside your key_name.

The `{i}` will act as placeholder that will be replaced by the index of your field, starting from zero.

```python
from StructNoSQL import TableDataModel, MapModel, BaseField, ActiveSelf
from typing import Dict

class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class ParameterModel(MapModel):
        childParameters = BaseField(field_type=Dict[str, ActiveSelf], key_name='childParameterKey{i}', max_nested_depth=8, required=False)
    parameters = BaseField(field_type=Dict[str, ParameterModel], key_name='parameterKey', required=False)
```

To access the nested fields of our example above, you will do the following :
```python
retrieved_first_nested_child_parameter = table.get_field(
    key_value='k42', field_path='parameters.{{parameterKey}}.childParameters.{{childParameterKey0}}', 
    query_kwargs={'parameterKey': 'exampleParameterId', 'childParameterKey0': 'firstNestedParameterId'}
)
retrieved_second_nested_child_parameter = table.get_field(
    key_value='k42', field_path='parameters.{{parameterKey}}.childParameters.{{childParameterKey0}}.childParameters.{{childParameterKey1}}',
    query_kwargs={'parameterKey': 'exampleParameterId', 'childParameterKey0': 'firstNestedParameterId', 'childParameterKey1': 'secondNestedParameterId'}
)
```

### Step 3 (optional) : Specifying a maximum nested depth 

You can (and probably should) limit the amount of times an item can nest himself by using the max_nested_depth attribute.
```python
childParameters = BaseField(field_type=Dict[str, ActiveSelf], key_name='childParameterKey{i}', max_nested_depth=8)
```

---

### The depth limit

DynamoDB imposes a 32 max nested depth for your objects. If you did not specify the max_nested_depth, StructNoSQL will 
construct your recursive fields until the 32 depth limit.

#### 32 depth level limit != 32 nesting limit
Consider the following model
```python 
class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
        class ParameterModel(MapModel):
            childParameters = BaseField(field_type=Dict[str, ActiveSelf], key_name='childParameterKey{i}', required=False)
        parameters = BaseField(field_type=Dict[str, ParameterModel], key_name='parameterKey', required=False)
    friends = BaseField(field_type=Dict[str, FriendModel], key_name='friendId', required=False)
```


If we wanted to access the parameters field of an item in the friends object, we would need to do
```python
table.get_field(field_path='friends.{{friendId}}.parameters', query_kwargs={'friendId': 'exampleFriendId'})
```
In our field_path, we have specified three items paths (each separated by a dot), which means, that the parameters item 
is at a depth of 3. Notice how since the ```friends``` field is a dictionary, it requires two level of depth to access 
an item inside the friends object. It will be the same for list's or set's, it is simply the way DynamoDB structure your 
data.

Let's say we wanted to access the second nested child parameters we would do :
```python
table.get_field(
    key_value='k42', field_path='friends.{{friendId}}.parameters.{{parameterKey}}.childParameters.{{childParameterKey0}}.childParameters.{{childParametersKey1}}',
    query_kwargs={'parameterKey': 'exampleParameterId', 'childParameterKey0': 'firstNestedParameterId', 'childParameterKey1': 'secondNestedParameterId'}
)
```
If you count the amount of field paths we specified, we are already at a depth of 8.
```childParameterKey0``` is at a depth of 4, ```childParameterKey1``` at a depth of 6, ```childParameterKey2``` at a 
depth of 8, until the last nested item that StructNoSQL will be able to create, which will be ```childParameterKey14``` 
who will be exactly at the limit depth of 32.

If you try to manually set a max_nested_depth that would make your model go above the depth limit of 32, StructNoSQL
will only create your fields recursively until it hits the limit of 32. Above which, your fields will not be created
and so will cause a ```FieldNotFound``` exception if you try to access them.

:::info Any way to override the depth limit ?
No, it is imposed by DynamoDB. The limit of 32 depth levels, even tough can seems small, is actually enormous.
If you need more depth than that, you could consider flattening your data, which has a lot of advantages, including
giving you virtually unlimited depth. Read the NoSQL design principles to learn more : NOT YET WRITTEN
:::


## Full Example 

### Queried record
```json
{
  "userId": "x42",
  "parameters": {
    "exampleParameterId": {
      "childParameters": {
        "firstNestedParameterId": {
          "parameterValue": 23,
          "childParameters": {
            "secondNestedParameterId": {
              "parameterValue": 9421
            }
          }
        }
      }
    }
  }
}
```

### Code
```python
from StructNoSQL import TableDataModel, DynamoDBBasicTable, PrimaryIndex, BaseField, MapModel, ActiveSelf
from typing import Dict


class UsersTableModel(TableDataModel):
    userId = BaseField(field_type=str, required=True)
    class ParameterModel(MapModel):
        childParameters = BaseField(field_type=Dict[str, ActiveSelf], key_name='childParameterKey{i}', max_nested_depth=8, required=False)
    parameters = BaseField(field_type=Dict[str, ParameterModel], key_name='parameterKey', required=False)


class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel, primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

retrieved_second_nested_child_parameter = table_client.get_field(
    key_value='k42', field_path='parameters.{{parameterKey}}.childParameters.{{childParameterKey0}}.childParameters.{{childParameterKey1}}',
    query_kwargs={'parameterKey': 'exampleParameterId', 'childParameterKey0': 'firstNestedParameterId', 'childParameterKey1': 'secondNestedParameterId'}
)
print(retrieved_second_nested_child_parameter)

```

### Output
```
{'parameterValue': 9421}
```
        
