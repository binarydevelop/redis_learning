from redis_connection import redis_client
import random
from datetime import datetime, timedelta

# this is a blocking code 
def track_event(event_type, page):
    redis_client.incr(f"analytics:{page}:{event_type}:total")
    
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    redis_client.incr(f"analytics:{page}:{event_type}:{timestamp}")
    
def get_total_events(event_type, page):
    total = redis_client.get(f"analytics:{page}:{event_type}:total")
    
    return int(total) if total else 0

def get_last_n_minutes(event_type, page, minutes = 5):
    now = datetime.now()
    
    total = 0
    
    for i in range(minutes):
        ts = (now - timedelta(minutes= i)).strftime("%Y-%m-%d-%H-%M")
        key = f"analytics:{page}:{event_type}:{ts}"
        count = redis_client.get(key)
        total += int(count) if count else 0
    return total

def get_top_pages(event_type, minutes = 60):
    now = datetime.now()
    pages= {}
    
    for i in range(minutes):
        ts = (now - timedelta(minutes=i)).strftime("%Y-%m-%d-%H-%M")
        pattern = f"analytics:*:{event_type}:{ts}"
        
        for key in redis_client.scan_iter(match=pattern):
            parts = key.split(':')
            page = parts[1]
            count = int(redis_client.get(key) or 0)
            print(count, '@@@@')
            pages[page] = pages.get(page, 0) + count 
            
    return sorted(pages.items(), key=lambda x: x[1], reverse=True) 
    
pages = ["home", "about", "products", "contact"]
events = ["views", "clicks"]

# for _ in range(200):
#     page = random.choice(pages)
#     event = random.choice(events)
#     track_event(event, page)

# for _ in range(10):
#     event = random.choice(events)
#     page = random.choice(pages)
#     print(f"{page}:{event}", get_total_events(event_type=event, page= page))

# print(get_last_n_minutes("views", "home", minutes=60))
print(get_top_pages("clicks"))