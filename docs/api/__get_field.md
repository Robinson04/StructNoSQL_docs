---
id: get_field
slug: /api/get_field
---

**Allow to retrieve a single or multiple fields from your table.**

```python
table_client.get_field(key_value=str, field_path=str, query_kwargs=dict)
```

## Parameters

| Property name | Required | Accepted types | Description |
| ------------- | :------: | :------------: | :---------- |
| key_name      | YES      | str  | The key\_name of the primary or secondary index that will be used to find the record you want to perform the operation onto. It will usually be the primary index field (like userId or id) that you defined. _Note : The selection with secondary indexes is still in Beta and not fully working, see https://github.com/Robinson04/StructNoSQL/issues/10_ |
| key_value     | YES      | Any  | The record selector value for your operation. Will need to be of the same type as the type you defined the index field you specified with the key_name parameter, otherwise, you will get a DataValidation error. |
| field_path    | YES      | str  | The path expression to target the attribute to set/update in your record. See [Field path selectors](../basics/field_path_selectors.md) |
| query_kwargs  | NO       | dict | Used to pass data to populate a field_path that contains keys. See example below  : |


## Single field retrieving
{{sampler::get_field/single_selection}}

## Multi fields selectors

If you need to access multiple items that share the same location, you can use a multi-selector. In the ```field_path```
specify the attributes you want to retrieved by enclosing them in brackets and with a comma separating each attribute.
For example : ```myItem.(attribute1, attribute2, attribute3)```

:::tip
A single database request will be constructed and send to retrieve your multiple attributes. It is then more efficient 
to use multi selectors or the [```get_multiple_fields```](./get_multiple_fields) operation as much as you can, instead of sending multiple 
operations to your database to retrieve the data you need.
:::

You cannot use a multi-selector to get multiple fields that are not in the same location. For that use case, you need
the ```get_multiple_fields``` operation.


{{sampler::get_field/multi_selectors}}
 