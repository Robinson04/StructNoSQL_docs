---
id: introduction
title: Introduction
slug: /
---


### StructNoSQL

Structured document based Python NoSQL client for AWS DynamoDB with automatic data validation 
and advanced database queries functions. Compatible with Serverless applications.

### Use cases :



### Pre-requisites :

- A basic understanding of Python 3
- Understanding of the concept of databases
- Understanding of json like model of data
- An AWS Account

### Structure of the documentation

#### API Section
_The section you will use the most once using StructNoSQL_

Each functionality of the library and all of their details are documented in the API section, with one or multiple fully
working code samples per functionality that can be copied and paste, and that we regularly run as unit tests to guarantee 
they work as expected.

#### Details section:

Various details regarding performances, architecture, and the inner workings of StructNoSQL, that can be good to know,
yet are not required to know in order to fully use the library. 

### MongoDB comparison :

| Capability                                   | StructNoSQL | MongoDB |
| -------------------------------------------- | :---------: | :-----: | 
| Document based modelling of NoSQL databases  | ✅          | ✅  
| Automatic data validation                    | ✅          | ✅  
| Advanced database queries functions          | ✅          | ✅  
| Usable with Python                           | ✅          | ✅  
| Usable with any programming language         | ⬜           | ✅  
| Can operate as fully serverless              | ✅          | ⬜  
| Usable on AWS databases                      | ✅          | ✅ 
| Usable on Microsoft Azure databases          | ⬜           | ✅ 
| Usable on Google Cloud databases             | ⬜           | ✅ 
| World's most adopted NoSQL database client   | ⬜           | ✅ 



StructNoSQL achieve a similar goal as MongoDB, structuring NoSQL databases as modeled document databases with automatic 
data validation and advanced database queries functions. Unlike MongoDB, who operate as a C++ software running on a server 
separated from your application, which will act as an intermediary between your application and your database, and be an 
accessible trough an API trough any programming language; StructNoSQL operate as a Python library running directly with 
your application, without requiring an intermediary server, in such providing a greater flexibility with your 
infrastructure, in particular for Serverless applications, but being only usable with Python.

StructNoSQL currently only support DynamoDB on AWS, whereas MongoDB support various cloud providers like AWS, Google 
Cloud and Microsoft Azure.

StructNoSQL operate as a Python library, only directly usable by Python applications, whereas MongoDB operate as a C++ 
software accessible behind an API and so usable with any programming language.

MongoDB is a highly mature and adopted product. If the comparaisons cited above are not of a big importance to you, you 
will most certainly be better off using MongoDB rather than StructNoSQL.


### Contraintes :
