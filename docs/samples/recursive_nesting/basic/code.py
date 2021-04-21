from StructNoSQL import TableDataModel, BasicTable, PrimaryIndex, BaseField, MapModel, ActiveSelf
from typing import Dict


class UsersTableModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    class ParameterModel(MapModel):
        childParameters = BaseField(name='childParameters', field_type=Dict[str, ActiveSelf], key_name='childParameterKey{i}', max_nested_depth=8, required=False)
    parameters = BaseField(name='parameters', field_type=Dict[str, ParameterModel], key_name='parameterKey', required=False)


class UsersTable(BasicTable):
    def __init__(self):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name='accounts-data', region_name='eu-west-2',
            data_model=UsersTableModel(), primary_index=primary_index,
            auto_create_table=True
        )


table_client = UsersTable()

retrieved_second_nested_child_parameter = table_client.get_field(
    key_value='k42', field_path='parameters.{{parameterKey}}.childParameters.{{childParameterKey0}}.childParameters.{{childParameterKey1}}',
    query_kwargs={'parameterKey': 'exampleParameterId', 'childParameterKey0': 'firstNestedParameterId', 'childParameterKey1': 'secondNestedParameterId'}
)
print(retrieved_second_nested_child_parameter)
