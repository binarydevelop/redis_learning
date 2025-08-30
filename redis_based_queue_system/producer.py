import threading
import time
import json
from redis_connection import redis_client
from helpers import generate_random_string_with_repetition


def create_task(task_id):
    """Generate a single task dict"""
    return {
        "id": f"task-{task_id}",
        "work": generate_random_string_with_repetition(10)
    }


def producer(count=50):
    """Continuously push tasks into Redis queue"""
    for i in range(count):
        task = create_task(i)
        print(redis_client.lpush("queue", json.dumps(task)))  # enqueue
        print(f"Produced: {task['id']}")
    print("Producer finished adding tasks")



producer_thread = threading.Thread(target=producer, args=(100000000, ))
    
    # start threads
producer_thread.start()


    # wait for all threads
producer_thread.join()

