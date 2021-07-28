You can use {{operation_link}} to {{alteration_type}} multiple fields from different places.
Like ```{{type_operation_single}}```, you select by its primary key value the record you want to {{alteration_type}} 
fields from, with the ```key_value``` parameter.
Specify the different fields you want to {{alteration_type}} by passing a dictionary of 
[FieldRemover](../api/FieldRemover).
Similarly to ```{{type_operation_single}}```, each [FieldRemover](../api/FieldRemover) requires the field_path 
parameter, and has an optional query_kwargs parameter.