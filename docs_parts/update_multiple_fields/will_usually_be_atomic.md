:::tip Will usually be Atomic
Any setter that does not pass data validation will be discarded client side by StructNoSQL, but since all of your valid 
setters will be grouped in a single operation, if a single of your setter is invalid and cause the operation to crash, 
all of your setters will be rejected/and reverted (for example, trying to access/modify a value inside a field that 
should be a dict, where it is in reality a list)
:::