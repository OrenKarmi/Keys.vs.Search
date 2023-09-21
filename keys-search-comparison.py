import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query
import json
import time
from load_keys import connect
from load_keys import create_index


def main():
    # Connect to Redis
    r1 = connect('redis-10645.karmi1-cluster.primary.cs.redislabs.com', 10645)

    # Create JSON and HASH indexes for users
    rs_json = create_index(r1, "idx:json_users", IndexType.JSON)
    rs_hash = create_index(r1, "idx:hash_users", IndexType.HASH)

    # Perform the comparison
    # *** KEYS ***
    # measure the time elapsed for the scan/ keys query
    start_time = time.time()
    res = r1.keys(pattern='user:hash:40000*')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"KEYS Result is: ",res)
    print(f"*** KEYS Elapsed time: {elapsed_time:.4f} seconds")

    # *** JSON ***
    # measure the time elapsed for the search query
    start_time = time.time()
    # Search name and age range
    res = rs_json.search(
            Query("Paul @age:[400001 400009]")
            )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"FT.SEARCH for JSON Result is: ",res)
    print(f"*** JSON Search Elapsed time: {elapsed_time:.4f} seconds")

    # *** HASH ***
    # measure the time elapsed for the search query
    start_time = time.time()
    # Search name and age range
    res = rs_hash.search(
            Query("Paul @age:[400001 400009]")
            )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"FT.SEARCH for HASH Result is: ",res)
    print(f"*** HASH Search Elapsed time: {elapsed_time:.4f} seconds")


if __name__ == "__main__":
    # Call the main function when the script is executed
    main()
