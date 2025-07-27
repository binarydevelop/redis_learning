import asyncio
from config import is_async_redis_connected
from simulator import run_async_cache_simulation
from dotenv import load_dotenv

load_dotenv()

async def main():
    """Main async function"""
    print("🚀 Starting Async Redis Cache Simulation")
    
    # Check Redis connection
    if await is_async_redis_connected():
        print("✅ Async Redis connection established")
        try:
            # Run the async cache simulation
            await run_async_cache_simulation()
        except Exception as e:
            print(f"❌ Error in async simulation: {e}")
    else:
        print("❌ Failed to connect to Redis")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 