---
id: preventing-identifier-duplication-risks
title: Preventing identifier duplication risks
slug: /nosql-best-practices/preventing-identifier-duplication-risks
---

Even if you use UUID's as identifier in your database (like showcased in [Unique identifiers](./unique_ids.md)), each
time you need to use identifiers as keys (for example, in a dictionary field), you are going to face the risk of 
generating an identifier that is already being used inside your object, which will cause your old data to be overridden
if you try to update it to a new value.

If you use pseudo randoms identifiers (like showcased in [Unique identifiers](./unique_ids.md) your risks of identifier
duplications will be extremely low, and the one in a billion chance of overriding data is acceptable compared to the
additional database requests required to make sure you are not at risk of overriding data.

However, for crucial operations where identifier duplication and overriding data due to an id duplication would be 
catastrophic (for example, creating a project inside an account, where an identifier duplication would cause the 
previous project to de deleted), you should check that the identifier does not exist before creating your new field.

If you perform operation
inside an account where the risk of erasing data would not be catastrophic (for example, adding a new item into the
shopping cart of an user, where the worst case if a duplicate id is generated, is to override and remove another item
present in the cart), you can perform operations without worrying about id duplication.

You can do that by simply trying to retrieve the field you will be targeting before trying to update it, and only update
the field if the value you retrieved is None (hence, not found).

### Simple example
```python
from typing import Optional
import uuid

generated_id = str(uuid.uuid4())  # Generate an id
existing_project: Optional[dict] = table_client.get_field(
    key_value="x32", field_path='projects.{{projectId}}', 
    query_kwargs={'projectId': generated_id}
)  # Try to retrieve a project matching with the newly generated id

# continue, and so, another attempt will be made at generating a non-used identifier.
if existing_project is None:
    project_creation_success: bool = table_client.update_field(
        key_value="x32", field_path='projects.{{projectId}}',
        query_kwargs={'projectId': generated_id},
        value_to_set={'projectName': "My new project"}
    )
    print(f"Success : {project_creation_success}")
else:
    print(f"Identifier {generated_id} was already used")
```

---

### Complete bulletproof example

You could also go one step beyond, aim to be bulletproof, and prepare for the occurrence of an identifier duplication, 
by allowing multiple attempts to generate an identifier that is not already used.

```python
from StructNoSQL import TableDataModel, BaseField, MapModel, DynamoDBBasicTable, PrimaryIndex
from typing import Dict, Optional
import uuid

class TableModel(TableDataModel):
    id = BaseField(field_type=str, required=True)
    class ProjectModel(MapModel):
        name = BaseField(field_type=str, required=True)
    projects = BaseField(field_type=Dict[str, ProjectModel], key_name='projectId', required=False)

class UsersTable(DynamoDBBasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=TableModel, primary_index=primary_index,
            auto_create_table=True
        )

    def create_project(self) -> Optional[str]:
        # The range(10) loop below, is present to enforce a maximum of ten attempts to generate an 
        # non-used identifier, to avoid being stuck in an infinite loop if something goes terribly wrong.
        for i in range(10):
            generated_id = str(uuid.uuid4())  # Generate an id
            existing_project: Optional[dict] = self.get_field(
                key_value="x32", field_path='projects.{{projectId}}', 
                query_kwargs={'projectId': generated_id}
            )  # Try to retrieve a project matching with the newly generated id
            
            # If a project has been found, the below code will not execute, the loop will 
            # continue, and so, another attempt will be made at generating a non-used identifier.
            if existing_project is None:
                project_creation_success: bool = self.update_field(
                    key_value="x32", field_path='projects.{{projectId}}',
                    query_kwargs={'projectId': generated_id},
                    value_to_set={'projectName': "My new project"}
                )  # Try to create a new project
                
                if project_creation_success is True:
                    print("Identifier generation and project creation success")
                    return generated_id  # Return the generated_id and so exit the loop
                else:
                    print("Generated an non-used identifier but failed project creation")
                    # We do not continue the loop if an non-used identifier has been 
                    # generated but the creation of the project failed, because it is 
                    # not an issue coming from the identifier, but from somewhere else.
                    return None
        print("Could not generate an non-used identifier after ten attempts")
        return None
            
table_client = UsersTable()
created_project_id: Optional[str] = table_client.create_project()
```

Read more at : https://en.wikipedia.org/wiki/Universally_unique_identifier