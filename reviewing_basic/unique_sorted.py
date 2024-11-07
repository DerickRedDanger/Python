# Given a list of integers, write a function to return a list of unique numbers sorted in ascending order.
# Example: unique_sorted([4, 1, 3, 3, 4, 2]) should return [1, 2, 3, 4]

import random


# Creating the list to try the program
random_list = [random.randint(1,100) for _ in range (200)]

# Function to sort the unique numbers
def unique_sorted(nums: list) -> list:
    return sorted(set(nums)) # Sorted creates a new list with the iterable that was passed to it

print(unique_sorted(random_list))