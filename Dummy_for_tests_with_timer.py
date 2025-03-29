import timeit

code_to_test = """
from sortedcontainers import SortedList


def solution(intervals, queries):
    sorted_list_lists = SortedList(intervals)
    result = []
    for q, start, end in queries:
        if q == 0:
            idx_l = sorted_list_lists.bisect_left([start, 0]) -1  # position of the first element smaller then start
            idx_r = sorted_list_lists.bisect_right([end, 0])  # position of the last element smaller then end
            idx_l = 0 if idx_l < 0 else idx_l
            
            intersect = False
            for start_i, end_i in sorted_list_lists[idx_l: idx_r + 1]:
                if (start_i <= start <= end_i) or (start_i <= end <= end_i) or (start <= start_i <= end) or (start <= end_i <= end):
                    intersect = True
                    break
            result.append(intersect)
            
        elif q == 1:
            sorted_list_lists.discard([start, end])
            result.append(len(sorted_list_lists))
            
    return result

intervals = [[1, 3], [6, 8], [11, 13], [16, 18], [21, 23], [26, 28], [31, 33], [36, 38], [41, 43], [46, 48]]
queries = [[1, 1, 3], [1, 5, 7], [0, 9, 11], [1, 13, 15], [0, 17, 19], [0, 21, 23], [1, 25, 27], [1, 29, 31], [0, 33, 35], [0, 37, 39], [0, 41, 43], [0, 45, 47], [1, 49, 51], [1, 53, 55], [1, 57, 59], [0, 61, 63], [1, 65, 67], [0, 69, 71], [0, 73, 75], [0, 77, 79], [1, 81, 83], [1, 85, 87], [1, 89, 91], [0, 93, 95], [0, 97, 99]]
expected_result = [9, 9, True, 9, True, True, 9, 9, True, True, True, True, 9, 9, 9, False, 9, False, False, False, 9, 9, 9, False, False]

print(solution(intervals, queries))
print(expected_result)
"""


execution_time = timeit.timeit(code_to_test, number=1000)  # Runs the code 10 times
print(f"Execution time: {execution_time:.6f} seconds")