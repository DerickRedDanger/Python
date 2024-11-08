# Finding the maximum sum of a subarray of size k:

def max_sum_subarray(ar:list, k:int) ->int:
    if k > len(ar):
        return "Incorrect input, K can't be larger than the Array"
    
    left, right = 0, k -1
    current_sum = sum(ar[left:right +1])
    highest_sum = current_sum
    
    while right < len(ar) - 1:
        left += 1
        right += 1
        current_sum += ar[right] - ar[left-1]
        highest_sum = max(highest_sum,current_sum)
    
    return highest_sum

exercises =[
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], 3),
    ([10, -2, 3, -1, 5, -6, 7, 8, -9], 4),
    ([4, 2, -1, 6, -3, 5, 2, -5, 8], 2),
    ([1, -1, 1, -1, 1, -1, 1, -1, 1], 5),
    ([5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5], 6),
]

answer = [max_sum_subarray(ar:= exercise[0], k:= exercise[1]) for exercise in exercises]
print(answer)
