import random
import string


def generate_random_string_with_repetition(length):
    """Generates a random string of a given length with possible character repetition."""
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choices(characters, k=length))
    return random_string