import time

def retry(max_attempts=3, delay=1, backoff=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                attempts += 1
                print(f"Attempt {attempts} of {max_attempts}")
                
                try:
                    result = func(*args, **kwargs)  
                    print(f"Connection successful on attempt {attempts}")  
                    return result 
                except Exception as e:
                    print(f"Attempt {attempts} failed: {e}")
                    
                    if attempts < max_attempts:
                        print(f"Waiting {current_delay} seconds before retry...")
                        time.sleep(current_delay)
                        current_delay *= backoff  
                    else:
                        print("Max attempts reached, giving up")
                        return 
        return wrapper
    return decorator