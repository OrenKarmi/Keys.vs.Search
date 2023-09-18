import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query
import json
import time


# Connect
def connect(host,port):
    ## Connect
    r = redis.Redis(host=f"{host}", port=f"{port}", decode_responses=True)
    return r


def create_index(r):
    ## Define search schema
    schema = (
        TextField("$.name", as_name="name"),
        TagField("$.city", as_name="city"),
        NumericField("$.age", as_name="age")
    )
     
    ## Create an index
    rs = r.ft("idx:users")
    idx_name = "idx_name_init"
    json_string = "json_str_init"


    try:
        ## Check if the index exists
        idx_info = rs.info()
        idx_name = "idx:users"
    
        # Convert the JSON object to a string
        json_string = json.dumps(idx_info)
    
    except Exception as e:
        # The index already exist
        a=1

    if idx_name in json_string:
        a=1
        # index already exists
    else:
        # creating idx:users
        rs.create_index(
            schema,
            definition=IndexDefinition(
                prefix=["user:"], index_type=IndexType.JSON
            )
        )
    return rs
    

def main():
    # Connect to Redis
    r1 = connect('redis-12087.karmi1-cluster.primary.cs.redislabs.com', 12087)

    # Create an index for users
    rs = create_index(r1)

    # measure the time elapsed for the scan/ keys query
    start_time = time.time()
    res = r1.keys(pattern='user:40000*')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result is: ",res)
    print(f"Elapsed time: {elapsed_time:.4f} seconds")

    # measure the time elapsed for the search query
    start_time = time.time()
    # Search name and age range
    res = rs.search(
            Query("Paul @age:[400001 400009]")
            )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result is: ",res)
    print(f"Elapsed time: {elapsed_time:.4f} seconds")


if __name__ == "__main__":
    # Call the main function when the script is executed
    main()



