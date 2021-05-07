---
id: unique-ids
title: Unique ids
slug: /nosql-best-practices/unique-ids
---

If you come from an SQL background, you likely used a lot of counters as identifiers. 

For example, let's picture the following records : 

```json
[
  {"id": 0, "name": "Paul", "friends": [2]},
  {"id": 1, "name": "Shakur", "friends": [0]},
  {"id": 2, "name": "Anthony", "friends": [0, 1]}
]
```

We use the id's of each person to identify them as friends.

Paul is friend with Anthony. Shakur is friend with Paul. And Anthony is friend with both Paul and Shakur.

Since our id's are being actively being used to reference a person, we should never change the id of a person. 
Otherwise, we would also need to check all records in the database, and update the id we modified if the person is 
friend with that person.

---

### Fallbacks of counter identifiers

This design, as innocent as it can be, will lead to huge issues if you ever need to merge tables together.

Let's picture you have one table for Europe, one for Asia, and another for America.

#### Europe table :
```json
[
  {"id": 0, "name": "Paul", "friends": [2]},
  {"id": 1, "name": "Shakur", "friends": [0]},
  {"id": 2, "name": "Anthony", "friends": [0, 1]}
]
```

#### Asia table :
```json
[
  {"id": 0, "name": "Baichuan", "friends": [2, 1]},
  {"id": 1, "name": "Shuai", "friends": [0]},
  {"id": 2, "name": "Jingjin", "friends": [0]}
]
```

#### America table :
```json
[
  {"id": 0, "name": "Mike", "friends": []},
  {"id": 1, "name": "Sam", "friends": [2]},
  {"id": 2, "name": "Pablo", "friends": [1]}
]
```

All three tables will both work side by side, unfortunately, if we ever need to merge them, the id's of the different 
table will override each other.

---

### UUID's as the answer

Instead, you should follow the best practice of using UUID's as identifiers.

An UUID is a pseudo-random string with extremely low chance of duplication.

You can easily generate them with the following Python code : 
```python
import uuid  
# The uuid module is builtin within
# Python, no need to install it
id = str(uuid.uuid4())
```

The best practice you can follow to avoid encountering this problem is using uuids for your record. For example :

```json
[
  {"id": "fab4b188-4f32-4b96-9bd8-1bcf1505f176", "name": "Paul", "friends": [2]},
  {"id": "982484ab-7de9-48ba-acce-b5940c8b706c", "name": "Shakur", "friends": [0]},
  {"id": "5ec0821d-1920-4e80-a6ea-5b9c4b22fa2c", "name": "Anthony", "friends": [0, 1]}
]
```

where will be able to merge our table like so :

```json
[
  {"id": "fab4b188-4f32-4b96-9bd8-1bcf1505f176", "name": "Paul", "friends": ["5ec0821d-1920-4e80-a6ea-5b9c4b22fa2c"]},
  {"id": "982484ab-7de9-48ba-acce-b5940c8b706c", "name": "Shakur", "friends": ["fab4b188-4f32-4b96-9bd8-1bcf1505f176"]},
  {"id": "5ec0821d-1920-4e80-a6ea-5b9c4b22fa2c", "name": "Anthony", "friends": ["fab4b188-4f32-4b96-9bd8-1bcf1505f176", "982484ab-7de9-48ba-acce-b5940c8b706c"]}, 
  {"id": "fc7ed3d6-bd0b-4171-b4f7-e4e2295b4008", "name": "Baichuan", "friends": ["3506fd66-6c4a-4b73-9741-debc885b899c", "e244505e-3aa5-47c5-ac31-3aa1051bc077"]},
  {"id": "e244505e-3aa5-47c5-ac31-3aa1051bc077", "name": "Shuai", "friends": ["fc7ed3d6-bd0b-4171-b4f7-e4e2295b4008"]},
  {"id": "3506fd66-6c4a-4b73-9741-debc885b899c", "name": "Jingjin", "friends": ["fc7ed3d6-bd0b-4171-b4f7-e4e2295b4008"]}, 
  {"id": "0ae90748-b8b9-44c5-9a90-a203aee5ff75", "name": "Mike", "friends": []},
  {"id": "9d1209c6-2902-4941-ac49-9b91c52a413c", "name": "Sam", "friends": ["ebf69cd3-fefe-4e66-b2cd-d5268b832c59"]},
  {"id": "ebf69cd3-fefe-4e66-b2cd-d5268b832c59", "name": "Pablo", "friends": ["9d1209c6-2902-4941-ac49-9b91c52a413c"]}
]
```

## Risks of identifier duplication

UUID's are pseudo randomly generated, and have a very low risk of duplication, below one in a billion.

For operations where the occurrence of an identifier duplication would not be catastrophic (for example, adding a new item into the shopping cart 
of a user, where the worst case if a duplicate id is generated, is to override and remove another item present in the 
cart), do not feel the need to check if the identifier is already used. 

If you perform operations where overriding data due to an id duplication would be catastrophic (for example, creating a
project inside an account, where an identifier duplication would cause the previous project to de deleted), you
should check that the identifier does not exist before creating your new field, you can easily prevent identifier 
duplications. You can find all the details on preventing identifier duplications at 
[Preventing identifier duplication risks](./preventing_identifier_duplication_risks.md)


Read more at : https://en.wikipedia.org/wiki/Universally_unique_identifier