---
id: put_record
title: put_record
sidebar_label: put_record
slug: /api/put_record
---

**Put a new record in the database. The record_dict_data must contain the primaryKey (example: userId) of the table, 
and all the required fields of the model. Return the success of the operation with True or False.**

```python
success = table.put_record(record_dict_data={'userId': "testUserId", 'name': 'John'})
```

