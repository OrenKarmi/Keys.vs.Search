# Keys.vs.Search
Comparing performance of KEYS vs. FT.SEARCH with 1m documents

**Description**

This document compares the performance of the KEYS command with FT.SEARCH.

**Test Results**

Using **FT.SEARCH is x300 times faster than KEYS** / SCAN for searching 10 specific JSON documents out of a 1m keys database. (see Detailed Test Results below).

**Motivation/ Background**

Database cleanup - customer requests to compare the time to look for keys to delete based on a given pattern.

**Test environment**

**Cluster:** Redis Enterprise Software v6.4.2 installed on a cluster of 3 AWS t3.small nodes.

**Database:** 2GB with RediSearch and RedisJSON capabilities. 1 master shard with 1 replica.

**Test implementation:** Python script calls for KEYS and FT.SEARCH and print the elapsed time for each command. The script is executed on a cluster node other than the node with the master shard.

**JSON document used**:**
'id': 'user:400000',
'payload': None,
'json': '{"name":"Paul John",
"email":"paul.john@example.com",
"age":400000,
"city":"London"}'

**Number of keys** loaded to the database: 1m
 ** An incrementing value from 1 to 1,000,000 was used for the “user ID” and “age” to have 1m different document keys.
 
**Commands Compared**

Python commands used for searching users in the range of 400000 to 400009:
r.keys(pattern='user:40000*')
rs.search( Query("Paul @age:[400000 400009]") )

**KEYS vs. SCAN clarification:**

The SCAN command is preferred over the KEYS command whenever the application needs to scan the entire key space. SCAN allows iterating on parts of the key space, limiting the response size to a given COUNT, and allowing other (queued) commands to operate between SCAN iterations. The SCAN command, therefore, scans the entire key space slower than KEYS. Hence, KEYS was used for this test.

**Detailed Test Results**

ubuntu@ip-172-31-25-197:/tmp$ python3 search-scan-comparison.py
Result is:  ['user:400004', 'user:400008', 'user:400003', 'user:400005', 'user:400006', 'user:400000', 'user:400002', 'user:400007', 'user:40000', 'user:400001', 'user:400009']

**Elapsed time: 0.4153 seconds**

Result is:  Result{10 total, docs: [Document {'id': 'user:400000', 'payload': None, 'json': '{"name":"Paul John","email":"paul.john@example.com","age":400000,"city":"London"}'}, Document {'id': 'user:400001', 'payload': None, 'json': '{"name":"Paul John","email":"paul.john@example.com","age":400001,"city":"London"}'}, Document {'id': 'user:400002', 'payload': None, 'json': '{"name":"Paul John","email":"paul.john@example.com","age":400002,"city":"London"}'}, Document {'id': 'user:400003', 'payload': None, 'json': '{"name":"Paul John","email":"paul.john@example.com","age":400003,"city":"London"}'}, Document {'id': 'user:400004', 'payload': None, 'json': '{"name":"Paul John","email":"paul.john@example.com","age":400004,"city":"London"}'}, Document {'id': 'user:400005', 'payload': None, 'json': '{"name":"Paul John","email":"paul.john@example.com","age":400005,"city":"London"}'}, Document {'id': 'user:400006', 'payload': None, 'json': '{"name":"Paul John","email":"paul.john@example.com","age":400006,"city":"London"}'}, Document {'id': 'user:400007', 'payload': None, 'json': '{"name":"Paul John","email":"paul.john@example.com","age":400007,"city":"London"}'}, Document {'id': 'user:400008', 'payload': None, 'json': '{"name":"Paul John","email":"paul.john@example.com","age":400008,"city":"London"}'}, Document {'id': 'user:400009', 'payload': None, 'json': '{"name":"Paul John","email":"paul.john@example.com","age":400009,"city":"London"}'}]}

**Elapsed time: 0.0013 seconds**

