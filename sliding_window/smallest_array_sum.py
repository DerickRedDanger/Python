# Finding the smallest subarray with a sum greater than or equal to a given value

def smallest_array_sum(ar:list, k:int)->int:

    if not ar:
        return "Array's empty"
    
    if k <= 0:
        return "K can't be lower then 0"
    
    left, right = 0, 0
    smallest = float('inf')
    current_sum = ar[right]

    while True:

        if right < len(ar) -1 and current_sum < k:
            right += 1
            current_sum += ar[right]

        elif left <= len(ar) -1 and current_sum >= k:
            window_size = right - left  + 1

            smallest = min(smallest,window_size)
            if smallest == 1:
                return 1

            current_sum += - ar[left]
            left +=1

        else:
            if smallest == float('inf'):
                return "No sum of subarray reachest the target"
            
            return smallest

exercises=[
    ([2, 1, 5, 2, 3, 2],7),
    ([2, 3, 1, 2, 4, 3], 7),
    ([1, 4, 4], 8),
    ([1, 1, 1, 1, 1, 1, 1, 1], 3),
    ([4, 2, 2, 7, 8, 1, 2, 8, 10], 8),
    ([1, 2, 3], 8),
    ([], 7),
    ([3, 4, 6, 8, 9], -3),
]

answer = [smallest_array_sum(ar:= exercise[0], k := exercise[1]) for exercise in exercises]
print(answer)
        
