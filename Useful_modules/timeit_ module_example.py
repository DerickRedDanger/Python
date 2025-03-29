# How timeit Works:
# It runs the code multiple times to get a precise measurement.
# It reduces external noise (like background processes) that could affect execution time.
# It returns the total time taken for a given number of executions.

# Basic Usage
# You can use timeit in two ways:

# 1️⃣ Using the timeit Module in a Script

import timeit

code_to_test = """
from collections import defaultdict

def count_pairs(arr):
    count = defaultdict(int)
    for n in arr:
        count[n] += 1
    return sum(v * (v - 1) // 2 for v in count.values())

arr = [1, 1, 2, 2, 1, 3] * 10000
count_pairs(arr)
"""

execution_time = timeit.timeit(code_to_test, number=10)  # Runs the code 10 times
print(f"Execution time: {execution_time:.6f} seconds")

# Why Use number=10?

# Running once can give inconsistent results.
# Running multiple times averages out performance fluctuations.

# 2️⃣ Using timeit in the Interactive Console
# You can also use it directly in the Python shell:


# import timeit

print(timeit.timeit("sum([i for i in range(1000)])", number=10000))

# This will:

# Run the sum([...]) operation 10,000 times.
# Print the total time taken.

# 🆚 Comparing Two Approaches
# Let’s compare your original dictionary approach vs the defaultdict approach:

# import timeit
from collections import defaultdict
from collections import Counter

arr = [1, 1, 2, 2, 1, 3] * 10000  # Large input for testing

def with_dict():
    unique = {}
    for n in arr:
        if n not in unique:
            unique[n] = 0
        unique[n] += 1
    return sum(v * (v - 1) // 2 for v in unique.values())

def with_defaultdict():
    count = defaultdict(int)
    for n in arr:
        count[n] += 1
    return sum(v * (v - 1) // 2 for v in count.values())

def with_counter():
    count = Counter(arr)
    return sum(v * (v - 1) // 2 for v in count.values())

print("dict:", timeit.timeit(with_dict, number=10))
print("defaultdict:", timeit.timeit(with_defaultdict, number=10))
print("Counter:", timeit.timeit(with_counter, number=10))