"""
heapq - Python's Heap Queue (Priority Queue) Module

Description:
    The heapq module provides an implementation of the heap data structure, specifically a min-heap.
    A heap is a binary tree where the parent node is always smaller (in a min-heap) or larger (in a max-heap) than its children.
    This ensures efficient access to the smallest (or largest) element.

Common Uses:
    - Implementing priority queues
    - Efficiently finding the k-smallest or k-largest elements
    - Merging multiple sorted lists efficiently
    - Scheduling tasks (e.g., CPU scheduling)

Key Functions:
    - heapq.heapify(iterable)       # Converts a list into a min-heap in O(n) time
    - heapq.heappush(heap, item)    # Pushes an item onto the heap in O(log n) time
    - heapq.heappop(heap)           # Removes and returns the smallest item in O(log n) time
    - heapq.heappushpop(heap, item) # Pushes an item, then pops and returns the smallest (more efficient than push+pop)
    - heapq.nlargest(n, iterable)   # Returns the n largest elements in O(n log k) time
    - heapq.nsmallest(n, iterable)  # Returns the n smallest elements in O(n log k) time
"""

import heapq

# Example 1: Basic Heap Operations
def example_min_heap():
    heap = []
    heapq.heappush(heap, 10)
    heapq.heappush(heap, 5)
    heapq.heappush(heap, 20)

    print("Smallest element:", heapq.heappop(heap))  # Output: 5
    print("Remaining heap:", heap)  # Output: [10, 20]

# Example 2: Finding the k-smallest elements
def example_k_smallest():
    nums = [50, 10, 30, 20, 40]
    smallest_three = heapq.nsmallest(3, nums)  # Get 3 smallest numbers
    print("3 smallest elements:", smallest_three)  # Output: [10, 20, 30]

if __name__ == "__main__":
    example_min_heap()
    example_k_smallest()
