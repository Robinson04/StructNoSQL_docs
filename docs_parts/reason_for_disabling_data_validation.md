The retrieved data will be passed through the data validation of your table. If the value or
some parts of it are invalid, they will be removed. The data validation is unforced client side by StructNoSQL, not on 
the database side which might cause the retrieved_value to be None or have less items than is actually present in the 
database.

If you need to disable the data_validation and actually retrieve any data present in the database without any checks or
alterations being done, you can disable it by passing False to the ```data_validation``` parameter.