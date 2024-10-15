def Memoize(function):
    log = {}
    def wrapper(*args):
        if args not in log:
            log[args] = function(*args)
        return log[args]


    def get_log():
        return log
    
    wrapper.get_log = get_log
    return wrapper

@Memoize
def Fibonacci(n):

    if n == 0:
        return 0
    
    elif n == 1 or n == 2:
        return 1

    else:
        return Fibonacci(n-1) + Fibonacci(n-2)
    
print(Fibonacci(25))
print(Fibonacci(37))
print(Fibonacci(5))
print(Fibonacci.get_log())
