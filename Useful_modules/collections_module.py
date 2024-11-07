"""
collections Module - Specialized Data Structures

Introduction:
The 'collections' module implements specialized container datatypes that provide alternatives to Python's general-purpose built-in types.

Installation:
The collections module is part of the Python standard library, so no installation is required.

Basic Usage:
"""

from collections import defaultdict, namedtuple

# 1. defaultdict example
dd = defaultdict(int)
dd['a'] += 1
print(f"defaultdict: {dd}")

# returning it to a normal dictionary and getting only the values
# The slight overhead of converting to a standard dictionary for printing is usually negligible
print(f"dict: {dict(dd)}")


# 2. namedtuple example
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(f"Namedtuple point: {p.x}, {p.y}")

"""
Advanced Usage:
"""

# 1. deque (double-ended queue) example
from collections import deque
dq = deque([1, 2, 3])
dq.appendleft(0)
dq.append(4)
print(f"Deque after operations: {dq}")

"""
Real-World Example:
"""
# 1. Counter example - counting occurrences in a list
from collections import Counter
data = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
counter = Counter(data)
print(f"Item count: {counter}")
