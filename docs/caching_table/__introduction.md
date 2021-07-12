---
title: Introduction
---

StructNoSQL has mutliple types of table clients. The simplest (and the one used throughout most of the documentation)
is the ```DynamoDBBasicTable```.

The ```DynamoDBCachingTable``` will lower the amount of requests to your database, by grouping your operations as much as 
possible before sending a request to your database, and cache the data your retrieved from your database for re-use 
without needing to re-request it while keeping an in-memory representation of your data and performing your operations 
onto the cached data, even before the operations are sent to the database.

It can be used interchangeably with the ```DynamoDBBasicTable```, so the rest of the documentation still applies, with the
specific features of the DynamoDBBasicTable detailled here.

### Functionalities
- Groups update and delete operations to lower the amount of requests
- Does not group the get operations (since you need to data right away)
- Cache the retrieved data and will re-use it if re-requested
- In-memory representation of the data, where update and delete operations will be performed and cached, even before the
  operations are committed
- Require a call to the commit_operations function before operations are send
- Fully interchangeable with the ```DynamoDBBasicTable```, apart for the additional commit_operations function

### Use cases
- Round-turn applications where the commit_operations can easily be enforced at the end of a round (for example, the
  [inoft_vocal_framework](https://github.com/Robinson04/inoft_vocal_framework) a library to create cross-platform apps
  and games on vocal assistants, use the CachingTable, and will enforce the commit_operations before sending back the
  response to the vocal assistant).
- Multi-threaded applications where various requests at slightly various moments
- Any application where a cache and operations grouping system is making your life easier and not harder

### Pitfalls
- Realtime concurrent reading/writing to the same records where the cached data could possibly not reflect actual data 
  (for example, in realtime multi-users software)
  


