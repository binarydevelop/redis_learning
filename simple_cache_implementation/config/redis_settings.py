import redis
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Redis connection
try:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        username=os.getenv("REDIS_USERNAME"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True,
    )
except Exception as e:
    print(f"Error connecting to Redis: {e}")
    redis_client = None

