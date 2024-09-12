def Logging(function):
    log = []
    
    def wrapper(*args, **kwargs):
        log.append((function.__name__, args, kwargs))
        result = function(*args, **kwargs)
        return result
    
    def get_log():
        return log
    
    wrapper.get_log = get_log
    return wrapper

if __name__ == '__main__':
    @Logging
    def sum_and_multiply(*elements_to_sum, multiply=1):
        total_sum = sum(elements_to_sum)
        if isinstance(multiply, (int, float)):
            total_sum *= multiply
        print(total_sum)
        
    sum_and_multiply(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, multiply=5)
    sum_and_multiply(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, multiply=4)
    sum_and_multiply(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    sum_and_multiply(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, multiply='a')
    
    # Print the log
    print(sum_and_multiply.get_log())