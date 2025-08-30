import threading
import time
import json
from redis_connection import redis_client
from helpers import generate_random_string_with_repetition


def consumer(name):
    """Continuously consume tasks from Redis queue"""
    while True:
        # BRPOP blocks until a task is available
        task_data = redis_client.brpop("queue", timeout=10)
        if task_data:
            _, raw_task = task_data
            task = json.loads(raw_task)
            print(f"🔵 Consumer {name} processed {task['id']} → {task['work']}")
        else:
            print(f"⚠️ Consumer {name} timed out, exiting")
            break


consumer_threads = [
    threading.Thread(target=consumer, args=(f"C{i}",))
    for i in range(1)
]

for t in consumer_threads:
    t.start()
    
for t in consumer_threads:
    t.join()