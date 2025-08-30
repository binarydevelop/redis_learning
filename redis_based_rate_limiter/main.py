from redis_connection import redis_client
import random
from client import create_clients
import json

MAX_REQUEST = 3
TTL= 15

def check_count_of_requests(ip_address):
    number_of_requests = redis_client.get(ip_address) 
    if number_of_requests is None:
        return (False, 0)
    elif int(number_of_requests) < MAX_REQUEST:
        return (False, number_of_requests)
    elif int(number_of_requests) >= MAX_REQUEST:
        return (True, number_of_requests)
        
def update_request_count(ip_address, count):
    if count == 0:
        redis_client.expire(ip_address, TTL)

    redis_client.incr(ip_address)
    return None

def accept_connection(request):
    gt_max_req, number_of_request = check_count_of_requests(request["ip"])
    if gt_max_req:
        print(f"429 for {request['ip']}!")
    else:
        update_request_count(request["ip"], number_of_request )
        

#demo 

clients = create_clients(3)
for _ in range(20):
    client = random.choice(clients)
    accept_connection(request=client)
    