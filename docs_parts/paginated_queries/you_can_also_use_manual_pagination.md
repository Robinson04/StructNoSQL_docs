:::tip You can also use manual pagination
Notice that the operation has support for the exclusive_start_key, and each item of the records_paginator is a tuple
containing both the records_items and the query_metadata. This allows you to start you records_paginator at a specific
point to resume from a previous query operation, and you can save the last_evaluated_key of the query_metadata's to
continue your query operation later as detailed in [query_pagination](../basics/query_pagination)
:::