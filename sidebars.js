module.exports = {
  mainSidebar: {
    Basics: [
        'introduction',
        'basics/installation',
        'basics/creating_your_first_table',
        'basics/modeling_your_database',
        'basics/recursive_nesting'
    ],
    "Caching Table": [
        'caching_table/introduction',
        'caching_table/creating_a_caching_table',
        'caching_table/committing_operations',
        'caching_table/clearing_cache',
    ],
    "NoSQL best practices": [
        "nosql_best_practices/flattening-data",
        "nosql_best_practices/unique-ids",
        "nosql_best_practices/preventing-identifier-duplication-risks"
    ],
    API: [
        'api/put_record',
        'api/delete_record',
        'api/get_field',
        'api/get_multiple_fields',
        'api/query_field',
        'api/query_multiple_fields',
        'api/paginated_query_field',
        'api/paginated_query_multiple_fields',
        'api/update_field',
        'api/update_multiple_fields',
        'api/delete_field',
        'api/remove_field',
        'api/delete_multiple_fields',
        'api/remove_multiple_fields',
        'api/FieldGetter',
        'api/FieldSetter',
        'api/FieldRemover',
        'api/ActiveSelf',
        'api/commit_operations',
        'api/commit_update_operations',
        'api/commit_remove_operations',
    ],
    Details: [
        'performances',
        'reserved_words'
    ]
  },
};
