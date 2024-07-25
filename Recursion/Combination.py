from typing import List

# List of elements
lis = [1, 2, 3, 4,5, 6, 7, 8, 9]

# Number of elements per combination
k = 3


# Main function that generate all combinations of K elements from a list
# Initializing result to store the combination and calling the helper function to fill it
def combinations(lis: List[int], k: int) -> List[List[int]]:
    result = []
    generate_combinations(lis, k, 0, [], result)
    return result

# helper function that uses recursion to generate all combinations. 
# It takes the same parameters as combinations, plus two more:
# start, which is the index in lis where the current combination starts,
# and current_combination, which is the current combination being built.
def generate_combinations(lis: List[int], k: int, start: int, current_combination: List[List[int]], result: List[List[int]]) -> List[List[int]]:
    
    # Base case, if K == 0, then we've complete a combination, and add it to result
    if k == 0:
        result.append(current_combination[:])
        return
    
    # This loop goes through each element in lis starting from start.
    # For each element, it adds the element to current_combination, 
    # recursively calls generate_combinations to generate the rest of the 
    # combination, and then removes the element from current_combination.
    for i in range(start, len(lis)):
        current_combination.append(lis[i])
        generate_combinations(lis, k - 1, i + 1, current_combination, result)
        current_combination.pop()

# Short explanation:

"""
This function only create combinations because of it's helper function taking as input start = i+1 
This makes sure each recall to it start on the element after the last one explored, thus not allowing it to explore past elements
"""


# Explanation with example:
"""

Using as example a lis = [1, 2, 3, 4] and k = 3:

At the start, the helper function would get generate_combinations([1, 2, 3, 4], 3, 0, [], result)
Since start is 0, it's for would add the lis[0] (1 in this case) to the current combination
then recall itself with generate_combinations( lis = [1, 2, 3, 4], k = 2, start = 0 + 1, current_combination = [1], result)
Now that start is 1, inside it's for, it would add the lis[1] (2 now) to the current combination.
then it would recall itself with generate_combinations([1, 2, 3, 4],k = 1, start = 2, [1, 2], result)
add the lis[2] (3) to current_combination and recall itself with generate_combinations([1, 2, 3, 4], k = 0, start = 3, [1, 2, 3], result)
But now, since k == 0 our helper function will append the current_combination to results without recalling itself,
thus, moving back to the past call of this function, generate_combinations([1, 2, 3, 4],k = 1, start = 2, [1, 2], result)
Now result = [1, 2, 3], and inside the loop, current_combination pops it's last element and continues the loop
thus appending lis[3] (4) to curent combination_combination and recalling itself with generate_combinations([1, 2, 3, 4], k = 0, start = 3, [1, 2, 4], result = [1, 2, 3])
This funtion also have K==0, so it will append current_combination to result and move back to the past call.
The last call will then pop the 4 from the current_combination, but since it reached the end of the list, it will stop.
moving to the call before it, the generate_combinations([1, 2, 3, 4], 2, 1, [1], result)
it's combination was [1, 2], it will pop the last element and add lis[2], so combination =[1, 3], remember start = i + 1 = 4
leading it to call generate_combinations([1, 2, 3, 4], 2, 4, [1,3], result)
which leads it to add lis[3] to combination and eventually append [1, 3, 4] to results
and then backtracking to the combination = [1,3]. Continuing it's for, it will pop 3 and add 4 leading to combination = [1,4]
which would make start = 4+1 = 5 and calling the the function generate_combinations([1, 2, 3, 4], 1, 5, [1,4], result)
Inside this function, you may notice that inside it's for, the range is range(5,4), meaning it won't run.
making it stop and backtrack to the past call.
"""

# Example usage:
"""
lis = [1, 2, 3, 4]
k = 3
print(combinations(lis, k))  # Output: [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]
"""

# Version without comments
"""
lis = [1, 2, 3, 4,5, 6, 7, 8, 9]
k = 3

def combinations(lis: List[int], k: int) -> List[List[int]]:
    result = []
    generate_combinations(lis, k, 0, [], result)
    return result

def generate_combinations(lis: List[int], k: int, start: int, current_combination: List[List[int]], result: List[List[int]]) -> List[List[int]]:
    if k == 0:
        result.append(current_combination[:])
        return
    
    for i in range(start, len(lis)):
        current_combination.append(lis[i])
        generate_combinations(lis, k - 1, i + 1, current_combination, result)
        current_combination.pop()

print(combinations(lis, k))
"""