import time
from simple_redis_cache.helpers import generate_random_string_with_repetition
from simple_redis_cache.redis_connection import redis_client
def write_op(key, value = generate_random_string_with_repetition(5)):
    response = redis_client.set(key, value, ex = 30)
    
    if response:
        return True
    
    return False


def read_op(key):
    response = redis_client.get(key)
    
    if response:
        print(response)
    else:
        print('Fetching from the DB.')
        time.sleep(1)
        to_save = generate_random_string_with_repetition(5)
        redis_client.set(key, to_save)
        print(to_save)
        return to_save
        

while True:
    user_input = input("Enter 1 to read and 2 to write.")
    user_input_key = input("Enter key 🗝️")
    match user_input:
        case "1":
            read_op(user_input_key)
        case "2":
            write_op(user_input_key)


