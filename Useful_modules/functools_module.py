"""
functools Module - Higher-Order Functions and Operations

Introduction:
The 'functools' module provides higher-order functions that operate on or return other functions.

Installation:
The functools module is part of the Python standard library, so no installation is required.

Basic Usage:
"""

from functools import partial, lru_cache

# 1. Partial functions
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
print(f"Square of 5: {square(5)}")

# 2. Memoization with lru_cache
@lru_cache(maxsize=100)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print(f"Fibonacci(10): {fib(10)}")

"""
Advanced Usage:
"""

# 1. Using reduce to sum a list
from functools import reduce
result = reduce(lambda x, y: x + y, [1, 2, 3, 4])
print(f"Sum of list: {result}")

"""
Real-World Example:
"""
# Memoization for expensive recursive calls (like Fibonacci)
print(f"Memoized Fibonacci(20): {fib(20)}")
