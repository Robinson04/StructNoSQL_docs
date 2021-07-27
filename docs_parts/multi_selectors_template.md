When using a multi-selector, no matter what, ```{{variable_name}}``` will always be a dictionary containing all the names 
of all fields you requested as keys in the dictionary. 
Even if the operation failed, the dictionary will be returned with a ```None``` value for each field.
Since it is guaranteed that the keys will be present, you can access the retrieved values directly with brackets instead 
of using the ```.get``` function on your dictionary.