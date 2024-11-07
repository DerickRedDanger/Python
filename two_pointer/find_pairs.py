# Write a function to find the first pair of numbers in a sorted list that adds up to a given sum.
# Use the two-pointer technique.
# Example: find_pair([1, 2, 3, 4, 6], 6) should return (2, 4)


def find_pair(nums: list, target: int) -> tuple:
    if len(nums) < 2:
        return "List too short"
    
    left = 0
    right = len(nums) -1

    while left < right:
        current_sums = nums[left] + nums[right]
        if current_sums == target:
            return (nums[left], nums[right])
        
        elif current_sums > target:
            right -= 1

        else:
            left += 1

    return "It's not possible"
        
    

# Testing code:
# Format = (list, target)
tests = [
        ([1],2),
        ([1,2,3,4,5,6],12),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 10),
        ([10, 20, 30, 40, 50, 60, 70, 80, 90], 100),
        ([5, 7, 11, 15, 18, 22, 25, 30], 33)
        ]

answer = [find_pair(List := test[0], target := test[1]) for test in tests]

print(answer)