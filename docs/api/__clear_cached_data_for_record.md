---
id: clear_cached_data_for_record
slug: /api/clear_cached_data_for_record
---

**Clear all cached data for a single record selected by its primary key value in your [```CachingTable```](../caching_table/introduction.md)**

```python
table_client.clear_cached_data_for_record(record_primary_key=str)
```

{{file::../docs_parts/caching_table/only_usable_in_caching_table_warning.md}}

## Parameters

clear_cached_data_for_record has no parameters.
 
## Availability

{{file::../docs_parts/feature_availability_table/preset_only_caching.md}}

## Example

{{sampler::caching_table/commit_operations/basic}}
