---
id: committing_operations
title: Committing operations
---

The automatic grouping and caching of data happens under the hood when using a ```CachingTable``` and does not require
any modifications to your code comparing to using a ```DynamoDBBasicTable```.



:::warning Never forget to commit
There is no automatic fail-safe that will commit your operations at the end of the execution of your application. If you
forget to commit your operations, they will simply not be sent to the database.
:::


```python
table_client.commit_operations()  # Commit both the update and remove operations
table_client.commit_update_operations()  # Commit only the update operations
table_client.commit_remove_operations()  # Commit only the remove operations
```

:::info Don't be shy to commit
No request will be sent to your database if you commit your operations and there is nothing to commit. Do not hesitate 
to always commit your operations at different points in your application.
:::