from config import get_redis
import random
import string
import threading
import time

redis_client = get_redis()

def generate_user_dict(count, id_length=8):
    user_dict = {}
    for i in range(1, count + 1):
        rand_part = ''.join(random.choices(string.ascii_letters + string.digits, k=id_length))
        key = f"user-{i}"
        user_dict[key] = rand_part
    return user_dict

def set_redis_with_mock_data():
    """
        synchronously set mock data in Redis with progress feedback
    """
    user_data = generate_user_dict(1000)
    for key, value in user_data.items():
        redis_client.set(key, value)
    return None

def set_redis_with_mock_data_async(count=1000, batch_size=100):
    """
    Asynchronously set mock data in Redis with progress feedback
    """
    def _setup_data():
        try:
            print(f"Starting to set up {count} mock user records...")
            user_data = generate_user_dict(count)
            
            # Process in batches for better performance
            items = list(user_data.items())
            total_batches = (len(items) + batch_size - 1) 
            print(total_batches)
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(items))
                batch_items = items[start_idx:end_idx]
                
                # Set batch of items
                for key, value in batch_items:
                    redis_client.set(key, value)
                
                # Progress feedback
                progress = ((batch_num + 1) / total_batches) * 100
                print(f"Progress: {progress:.1f}% ({end_idx}/{count} records set)")
                
                # Small delay to prevent overwhelming Redis
                time.sleep(0.01)
            
            print(f"✅ Successfully set up {count} mock user records in Redis!")
            
        except Exception as e:
            print(f"❌ Error setting up mock data: {e}")
    
    # Start the setup in a background thread
    setup_thread = threading.Thread(target=_setup_data, daemon=True)
    setup_thread.start()
    
    return setup_thread

def set_redis_with_mock_data_batch(count=1000, batch_size=100):
    """
    Synchronous batch processing for better performance
    """
    print(f"Setting up {count} mock user records in batches of {batch_size}...")
    user_data = generate_user_dict(count)
    
    items = list(user_data.items())
    total_batches = (len(items) + batch_size - 1) // batch_size
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(items))
        batch_items = items[start_idx:end_idx]
        
        # Set batch of items
        for key, value in batch_items:
            redis_client.set(key, value)
        
        # Progress feedback
        progress = ((batch_num + 1) / total_batches) * 100
        print(f"Progress: {progress:.1f}% ({end_idx}/{count} records set)")
    
    print(f"✅ Successfully set up {count} mock user records!")
    return None