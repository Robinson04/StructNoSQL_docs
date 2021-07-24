:::warning Not always Atomic !
The data validation will be ran on the entirety of your data before starting to
send database requests. As explained in [Operations Sectioning](../details/operations_sectioning.md), if the sum of the 
size of all your setters exceeds 400KB (the DynamoDB limit per operation), your request will automatically be divided 
into multiple requests. If a/some part's of your operation are executed without causing a database rejection, and then 
one of the part of your operation is rejected, you will get a success value of False from the function call, yet, the 
parts of your operation that have already been completed, will not be reverted.
:::