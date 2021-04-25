---
id: creating_your_first_table
title: Creating your first table
---

Each table is composed of two parts.
- The table model (TableDataModel)
- The table client (BasicTable)

### Creating a table is done in 2 steps :


### Step 1 - The model of your table
For your table model, create a new class that inherit from TableDataModel. 

Create your first field, which will act as the primary key of your table.

Use the BaseField class. Specify the field name (like 'id' or 'userId') with the name parameter.

Use the field_type parameter to define which types will be acceptable for this field. The primary key of your table is 
a special in DynamoDB and cannot be of a complex type, but only of type str, int or float. Use a str type if you intend 
to use text values for you id's (for example if you use uuid's) and int or float if you use number based id's (for 
example, counter id's).

Set the required attribute to True. Since the field is at the root of your table, this means that each record in your 
database will require the 'userId' field to be present.

```python
from StructNoSQL import TableDataModel, BaseField

class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
```

### Step 2 : Create your table client

Add BasicTable and PrimaryIndex to your imports from StructNoSQL.

Create a new class that inherit from BasicTable (other table types exists).

Create a ```__init__``` function.

Create a PrimaryIndex and set the 'hash_key_name' property to the name you gave the field you want to use as your 
primary index. In our case, it is 'userId'.

Set the hash_key_variable_python_type to the field_type you used for your primary field. In our case str. Remember, an 
index field can only be of type str, int or float, and not of complex type.

Call the ```super().__init__```` function.

Pass it the ```table_name``` that will be used to create/find your database on AWS. You should not use the same table 
name twice for the same region on AWS. In our case, we will name our table ```my_first_table```.

Set the region in which your table will be created/find by passing an AWS region code name to the ```region_name``` 
parameter. We specified ```eu-west-2``` which is the code for the London region on AWS. You can find a list of the codes
of all the regions at [https://awsregion.info/](https://awsregion.info/)

Pass the primary_index object your created to the ```primary_index``` parameter.

Set auto_create_table to True or False. If it is True, if no table with the name and in the region you specified was 
found in your AWS account, the table will be created immediately. When a table is being created, your first requests
with StructNoSQL might failed and cause a 'TableInCreation' error, because a table can take up to 20 seconds to create.
If you prefer to manually create your tables, go to your AWS console, go to the DynamoDB service, and create a table
with the same name and in the same region as what you specified.

As the last parameter, pass an instance of your TableModel you created to the ````data_model``` parameter.

Finally, you can create an instance of your TableClient. We recommend that you use the same table instance to perform
multiple databases operations, because the initialization of the client is not instantaneous and take between a few
milliseconds and rarely up to tens of milliseconds.

```python
from StructNoSQL import TableDataModel, BaseField, BasicTable, PrimaryIndex

class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)

class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(
            hash_key_name='userId', 
            hash_key_variable_python_type=str
        )
        super().__init__(
            table_name="my-first-table", region_name="eu-west-2", 
            primary_index=primary_index, auto_create_table=True,
            data_model=UsersTableModel()
        )

table_client = UsersTable()
```

You can now fully perform operations on your table trough the table_client.
Right now, the model of your table only has an 'userId' field. 
Move to the next section to enrich your table model.gith