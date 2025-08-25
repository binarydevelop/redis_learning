from redis_connection import redis_client
import time
from helpers import generate_random_string_with_repetition

while True:
    user_input = input('Enter the key to be fetched.')
    
    if len(user_input) == 0:
        print('No key entered, Please retry.')
    elif user_input == 'q':
        print('Bye !')
        break
    else:
        response = redis_client.get(user_input)
        if response is None:
            print('Fetching from DB 🪣 It is slow')
            time.sleep(1)
            to_save = generate_random_string_with_repetition(5)
            print(redis_client.set(user_input, to_save,ex= 30))
            print(to_save)
        else:
            print(response)