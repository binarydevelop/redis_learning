"""Basic connection example.
"""

import redis

redis_client = redis.Redis(
    host='redis-17857.c281.us-east-1-2.ec2.redns.redis-cloud.com',
    port=17857,
    decode_responses=True,
    username="default",
    password="3QYPncFAxMUGyhPLc5i5aisWafdrHZL4",
)


redis_connection = redis_client.ping()

if redis_connection:
    print('Connection established. ')

