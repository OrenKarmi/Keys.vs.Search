import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query
import json
import time


# Connect to redis on host and port
def connect(host,port):
    ## Connect
    r = redis.Redis(host=f"{host}", port=f"{port}", decode_responses=True)
    return r

# Create an index
# Parameters:
# redis connection,
# name of the index to be created, and
# index_type - ENUM. Supported options: IndexType.HASH or IndexType.JSON
def create_index(r, index_name, index_type):
    ## Define search schema
    if index_type == IndexType.JSON:
        schema = (
                TextField("$.name", as_name="name"),
                TagField("$.city", as_name="city"),
                NumericField("$.age", as_name="age")
                )
    elif index_type == IndexType.HASH:
        schema = (
                TextField("name"),
                TagField("city"),
                NumericField("age")
                )
    else:
        # incorrect index type, use IndexType.HASH or IndexType.JSON
        return

    ## Create an index
    rs = r.ft(index_name)
    index_info_string = "str_init"

    try:
        ## Check if the index exists. Will throw an exception if not
        idx_info = rs.info()
        # Convert the JSON object to a string
        index_info_string = json.dumps(idx_info)

    except Exception as e:
        # The index already exist
        a=1

    if  index_name in index_info_string:
        # The index already exists
        a=1
    else:
        # creating idx:users
        rs.create_index(
            schema,
            definition=IndexDefinition(
                prefix=["user:"], index_type=index_type
            )
        )
    return rs

# Create json keys for users
# Users are different by ID and age (counter)
# Parameters:
# redis connection,
# Number of JSON document keys to create
def create_json_users(redis, number_of_users):
    ## Create users and set as json keys
    for i in range(1, number_of_users + 1):
        ## Creating user i with age i
        user = {
            "name": "Paul John",
            "email": "paul.john@example.com",
            "age": i,
            "city": "London"
        }
        ## Setting the user as json in Redis
        redis.json().set(f"user:json:{i}", Path.root_path(), user)


# Create Hash keys for users
# Users are different by ID and age (counter)
# Parameters:
# redis connection,
# Number of Hashes to create
def create_hash_users(redis, number_of_users):
    ## Create users and set as hash keys
    for i in range(1, number_of_users + 1):
        ## Creating user i with age i
        redis.hset(
                f"user:hash:{i}",
                mapping={
                    "name": "Paul John",
                    "email": "paul.john@example.com",
                    "age": i,
                    "city": "London"
                }
        )


def main():
    # Connect to Redis
    r1 = connect('redis-10645.karmi1-cluster.primary.cs.redislabs.com', 10645)

    # Create JSON and HASH indexes for users
    rs_json = create_index(r1, "idx:json_users", IndexType.JSON)
    rs_hash = create_index(r1, "idx:hash_users", IndexType.HASH)

    # Create users
    create_json_users(r1, 500000)
    create_hash_users(r1, 500000)


if __name__ == "__main__":
    # Call the main function when the script is executed
    main()




