from config import get_redis, is_redis_connected, redis_singleton


def main():
    if is_redis_connected():
        redis_client = get_redis()
        redis_client.set('foo', 'boo')
        print(redis_client.get('foo'))

if __name__ == "__main__":
    main()
    