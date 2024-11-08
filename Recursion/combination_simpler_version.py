def combination(arr:list, k:int) ->list[list]:

    # If the length of the combination is longer then the array, return empty
    if k > len(arr):
        return []

    # if there are no more elements to add, return a empty list and start backtracking
    if k == 0:
        return [[]]
    
    result = []
    for i in range(len(arr)):
        element = arr[i]
        remaining = arr[i+1:]
        for comb in (combination(remaining, k - 1)):
            result.append([element] +comb)

    return result

print(combination([1,2,3,4],3))