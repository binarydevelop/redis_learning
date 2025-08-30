import random 
from helpers import generate_random_string_with_repetition

def create_clients(count = 10):
    clients = []
    for _ in range(count):
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        request = {
            "ip": ip,
            "client_name": generate_random_string_with_repetition(5) 
        }
        clients.append(request)
    
    return clients