import heapq


def median(arr):
    min_heap, max_heap = [], []
    medians = []
    
    for num in arr:
        if max_heap and num < -max_heap[0]:
            heapq.heappush(max_heap, -num)
        else:
            heapq.heappush(min_heap, num)
        
        if len(max_heap) > len(min_heap):
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
        elif len(min_heap) > len(max_heap) + 1:
            heapq.heappush(max_heap, -heapq.heappop(min_heap))
        
        if len(min_heap) == len(max_heap):
            medians.append((-max_heap[0] + min_heap[0]) / 2)
        else:
            medians.append(min_heap[0])
    
    return medians