---
id: clear_cached_data_for_record
slug: /api/clear_cached_data_for_record
---

**Clear all cached values for a single record selected by its primary key value in your [```CachingTable```](../caching_table/introduction.md)**

```python
table_client.clear_cached_data_for_record(record_primary_key=str)
```

## Parameters

{{file::docs_parts/table_header.md::}}
{{file::docs_parts/record_primary_key_table_row.md::}}
 
## Availability

{{file::docs_parts/feature_availability_table/preset_only_caching.md::}}

## Example

{{sampler::../samples/caching_table/clear_cached_data_for_record/basic::}}
