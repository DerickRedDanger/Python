"""
itertools Module - Iterator Functions for Efficient Looping

Introduction:
The 'itertools' module provides fast, memory-efficient tools that are useful by working on iterators to produce complex iterators.

Installation:
The itertools module is part of the Python standard library, so no installation is required.

Basic Usage:
"""

import itertools

# 1. Combinations example
combinations = list(itertools.combinations([1, 2, 3], 2))
print(f"Combinations: {combinations}")

# 2. Infinite cycling through a list
cycle = itertools.cycle([1, 2, 3])
print(f"Cycle: {next(cycle)}, {next(cycle)}, {next(cycle)}, {next(cycle)}")

"""
Advanced Usage:
"""

# 1. Permutations
perms = list(itertools.permutations([1, 2, 3]))
print(f"Permutations: {perms}")

"""
Real-World Example:
"""
# Product of two lists
product = list(itertools.product([1, 2], ['a', 'b']))
print(f"Product of lists: {product}")
