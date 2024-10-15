"""
timeit Module - Measure Execution Time of Code Snippets

Introduction:
The 'timeit' module allows you to measure the execution time of small code snippets for performance testing and optimization.

Installation:
The timeit module is part of the Python standard library, so no installation is required.

Basic Usage:
"""

import timeit

# 1. Simple timing of a one-liner
time_taken = timeit.timeit('"-".join(str(n) for n in range(100))', number=1000)
print(f"Time taken for operation: {time_taken}")

"""
Advanced Usage:
"""

# 1. Timing a custom function
def my_function():
    return "-".join(str(n) for n in range(100))

print(f"Time taken by function: {timeit.timeit(my_function, number=1000)}")

"""
Real-World Example:
"""
# 1. Compare performance of list comprehension vs map
list_comp_time = timeit.timeit('[str(n) for n in range(100)]', number=1000)
map_time = timeit.timeit('list(map(str, range(100)))', number=1000)

print(f"List comprehension: {list_comp_time}, Map: {map_time}")
