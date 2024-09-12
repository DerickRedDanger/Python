import time

def Timer(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        val = function(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f'time needed to execute: {duration}')
        return val
    return wrapper

if __name__ == "__main__":
    @Timer
    def calculation(x, y):
        return x + y

    print(calculation(1, 2))