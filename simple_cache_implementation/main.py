from services import cache

if __name__ == '__main__':
    user_id = 'akjdfu3272sdmsf92knsdfm8'

cache.get_cached_data(user_id)

print('Second request')
cache.get_cached_data(user_id)