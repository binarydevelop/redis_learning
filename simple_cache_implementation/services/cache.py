import time
from config import redis_client
from dotenv import load_dotenv
import os

load_dotenv()

def get_data_from_db(key):
    """"Simulate DB call, process delay"""
    print('fetching data from db 🫙')
    time.sleep(2)
    return f"value for {key}"

def get_cached_data(key):
    """"Fetch data from cache"""
    print("Fetching data from cache")
    cached = redis_client.get(key)
    if cached is not None:
        print(f"Cache HIT: {key} -> {cached}")
        return cached
    
    else:
        print('Calling db for data')
        value = get_data_from_db(key)
        redis_client.set(key, value, ex=int(os.getenv("CACHE_TTL")))
        return value