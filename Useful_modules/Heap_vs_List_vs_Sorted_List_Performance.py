import heapq
import bisect
import time
import random

# Test size
N = 100_000  # You can increase this for more drastic results
test_data = list(range(1, N + 1))

# 1. Using a Heap (heapq)
def test_heapq():
    heap = test_data[:]  # Copy data
    heapq.heapify(heap)  # O(n) heapify

    start_time = time.time()
    for _ in range(N // 2):
        heapq.heappop(heap)  # Remove smallest (O(log n))
    end_time = time.time()
    
    print(f"Heapq time: {end_time - start_time:.4f} seconds")

# 2. Using a List (pop(0))
def test_list():
    lst = test_data[:]  # Copy data

    start_time = time.time()
    for _ in range(N // 2):
        lst.pop(0)  # Remove first element (O(n) per operation)
    end_time = time.time()
    
    print(f"List pop(0) time: {end_time - start_time:.4f} seconds")

# 3. Using a Sorted List (bisect.insort)
def test_sorted_list():
    sorted_list = []
    
    # Insert all elements one by one (O(n log n))
    for num in test_data:
        bisect.insort(sorted_list, num)  # O(n) worst case insert

    start_time = time.time()
    for _ in range(N // 2):
        sorted_list.pop(0)  # Remove smallest (O(1))
    end_time = time.time()
    
    print(f"Sorted List (bisect) time: {end_time - start_time:.4f} seconds")

# Run tests
if __name__ == "__main__":
    print(f"Testing with {N} elements:")
    test_heapq()
    test_list()
    test_sorted_list()
