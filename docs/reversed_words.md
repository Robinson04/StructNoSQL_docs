---
id: reserved_words
title: Reserved words
---


### Field names :

Restricted characters : 
- {
- }
- (
- )


### Expression attributes :

StructNoSQL will not immediately raise an Error if you use some reserved names imposed by DynamoDB. In which case, the
request will be sent to the database, rejected by DynamoDB, and StructNoSQL will raise an Error based on that.

Consult the following page for an up to date list of the reserved names of DynamoDB : 
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html