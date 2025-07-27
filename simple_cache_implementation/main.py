from config import get_redis, is_redis_connected, redis_singleton
from dotenv import load_dotenv
import os
from simulator import set_redis_with_mock_data_async, generate_user_dict
import time
import random
import string
load_dotenv()

redis_client = get_redis()

def generate_single_user_data(user_id, id_length=8):
    """Generate data for a specific user ID"""
    rand_part = ''.join(random.choices(string.ascii_letters + string.digits, k=id_length))
    return {user_id: rand_part}

def main():
    if is_redis_connected():
        try:
            setup_thread = set_redis_with_mock_data_async(count=1000, batch_size=100)
            print("🎯 Mock data setup started in background. You can start using the app immediately!")
        except Exception as e:
            print(f"Error occurred while setting mock data.{e}")

    while True:
        user_input = input("Enter user-id to fetch or q to quit: ")
        
        if not user_input or user_input == 'q':
            break
        else:
            try:
                result = redis_client.get(user_input)
                if not result:
                    time.sleep(2)
                    print('Fetching from db..')
                    # Generate data for the specific user ID that was requested
                    user_data = generate_single_user_data(user_input)
                    # Store the data with the correct user ID
                    for key, value in user_data.items():
                        print(key, value)
                        redis_client.set(key, value)
                        print(f"Stored: {key} = {value}")
                else:
                    print(f"Found in cache: {user_input} = {result}")
            except Exception as e:
                print(e)
    

if __name__ == "__main__":
    main()
    