def default_values(*arg, default = 0):
    numbers = [item for item in arg if isinstance(item,(int))]
    result = default
    if numbers:
        result = sum(numbers)
    print(result)
    
default_values('a','b','c','d',0.57,0.97)
default_values('a','b','c','d',0.57,0.97, default = 10)
default_values(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, default = 10)