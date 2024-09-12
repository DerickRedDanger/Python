def sum_and_multiply(*elements_to_sum, multiply=1):
    total_sum = sum(elements_to_sum)
    if isinstance(multiply, (int, float)):
        total_sum *= multiply
    print(total_sum)
    
    
sum_and_multiply(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, multiply = 5)
sum_and_multiply(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, multiply = 4)
sum_and_multiply(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,)
sum_and_multiply(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, multiply = 'a')