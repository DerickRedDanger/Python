def permutation(arr:list, k:int = -1) -> list[list]:
    
    # if K == 0, returns a empty list and backtrack
    if k == 0:
        return [[]]

    elif k == -1:
        k = len(arr)

    result = []
    for i in range(len(arr)):
        element = arr[i]
        remaining = [ char for char in arr if char != element]
        for perm in (permutation(remaining, k - 1)):
            result.append( [element] + perm)
    
    return result


print(permutation([1, 2, 3, 4, 5, 6],3))
        