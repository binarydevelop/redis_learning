import string
import uuid
from redis_connection import redis_client
import json
import time 
from helpers import generate_random_string_with_repetition
SESSION_TTL = 30
SESSION_PREFIX = "session:"

def create_session(userId, username):
    session_id = generate_random_string_with_repetition(11)
    session_key = SESSION_PREFIX + session_id 
    
    session_data = {
        "user_name": username, 
        "user_id": userId
    }
    redis_client.setex(session_key, SESSION_TTL, json.dumps(session_data))
    print(f"session created for user{username} with id {userId}: {session_id}")
    return session_id


def get_session(session_id):
    session_key = SESSION_PREFIX + session_id
    
    data = redis_client.get(session_key)
    
    if data is None:
        print('Session not found or expired.')
        return None
        
    return data

def destroy_session(session_id):
    session_key = SESSION_PREFIX + session_id
    
    is_deleted = redis_client.delete(session_key)
    
    if is_deleted:
        print('Session destroyed !')
        

# 1. User logs in -> create session
session_id = create_session(101, "alice")

# 2. Retrieve session
print("👉 Fetching session immediately:")
print(get_session(session_id))  # should return Alice’s session

# 3. Wait for TTL to expire
print("\n⏳ Waiting 15 seconds for session to expire...")
time.sleep(15)

print("👉 Fetching session after expiry:")
print(get_session(session_id))  # should be None

# 4. Create another session and logout
session_id2 = create_session(102, "bob")
print("👉 Bob’s session data:", get_session(session_id2))
destroy_session(session_id2)
print("👉 After logout:", get_session(session_id2))