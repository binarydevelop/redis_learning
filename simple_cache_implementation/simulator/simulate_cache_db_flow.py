from config import get_redis, get_async_redis
import random
import string
import threading
import time
import asyncio

redis_client = get_redis()

def generate_user_dict(count, id_length=8):
    user_dict = {}
    for i in range(1, count + 1):
        rand_part = ''.join(random.choices(string.ascii_letters + string.digits, k=id_length))
        key = f"user-{i}"
        user_dict[key] = rand_part
    return user_dict

def set_redis_with_mock_data():
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

# Async versions using asyncio and aioredis
async def generate_user_dict_async(count, id_length=8):
    """Async version of user dict generation"""
    user_dict = {}
    for i in range(1, count + 1):
        rand_part = ''.join(random.choices(string.ascii_letters + string.digits, k=id_length))
        key = f"user-{i}"
        user_dict[key] = rand_part
    return user_dict

async def set_redis_with_mock_data_async_aioredis(count=1000, batch_size=100):
    """
    True async version using aioredis and asyncio
    """
    try:
        print(f"🚀 Starting async setup of {count} mock user records...")
        redis_client_async = await get_async_redis()
        user_data = await generate_user_dict_async(count)
        
        # Process in batches for better performance
        items = list(user_data.items())
        total_batches = (len(items) + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(items))
            batch_items = items[start_idx:end_idx]
            
            # Create pipeline for batch operations
            pipeline = redis_client_async.pipeline()
            for key, value in batch_items:
                pipeline.set(key, value)
            
            # Execute batch
            await pipeline.execute()
            
            # Progress feedback
            progress = ((batch_num + 1) / total_batches) * 100
            print(f"📊 Progress: {progress:.1f}% ({end_idx}/{count} records set)")
            
            # Small delay to prevent overwhelming Redis
            await asyncio.sleep(0.01)
        
        print(f"✅ Successfully set up {count} mock user records using async Redis!")
        
    except Exception as e:
        print(f"❌ Error setting up mock data: {e}")

async def get_user_data_async(user_id):
    """
    Async function to get user data with cache-aside pattern
    """
    try:
        redis_client_async = await get_async_redis()
        
        # Try to get from cache first
        result = await redis_client_async.get(user_id)
        
        if result:
            print(f"🎯 Found in cache: {user_id} = {result}")
            return result
        else:
            # Cache miss - simulate database fetch
            print(f"⏳ Cache miss for {user_id}, fetching from database...")
            await asyncio.sleep(2)  # Simulate database delay
            
            # Generate new user data
            rand_part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user_data = {user_id: rand_part}
            
            # Store in cache
            for key, value in user_data.items():
                await redis_client_async.set(key, value)
                print(f"💾 Stored in cache: {key} = {value}")
            
            return rand_part
            
    except Exception as e:
        print(f"❌ Error getting user data: {e}")
        return None

async def run_async_cache_simulation():
    """
    Main async function to run the cache simulation
    """
    # Setup mock data
    await set_redis_with_mock_data_async_aioredis(count=1000, batch_size=100)
    
    print("\n🎮 Async Cache Simulation Ready!")
    print("Enter user IDs to test (e.g., user-1, user-123) or 'q' to quit")
    
    while True:
        try:
            # Use asyncio to handle input without blocking
            user_input = await asyncio.get_event_loop().run_in_executor(
                None, input, "Enter user-id to fetch or q to quit: "
            )
            
            if not user_input or user_input == 'q':
                break
            
            # Get user data asynchronously
            result = await get_user_data_async(user_input)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            
def generate_single_user_data(user_id, id_length=8):
    """Generate data for a specific user ID"""
    rand_part = ''.join(random.choices(string.ascii_letters + string.digits, k=id_length))
    return {user_id: rand_part}