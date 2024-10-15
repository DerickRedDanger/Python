n_retries = 5

def retry(function):
    def wrapper(*args, **kwargs):
        for _ in range(n_retries):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                print(f'Exception occurred: {e}')

        print(f'The function failed to run {n_retries} times.')
        return None
    return wrapper


import random

@retry
def test_function():
    if random.choice([True, False]):
        raise ValueError("Random failure!")
    return "Success!"

print(test_function())