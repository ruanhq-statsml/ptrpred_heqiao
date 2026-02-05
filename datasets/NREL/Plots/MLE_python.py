#python MLE 

import heapq
from collections import Counter
def topKFrequent(nums, k):
    count = Counter(nums)
    heap = []
    for num, freq in count.items():
    	heapq.heappush(heap, (freq, num))
    	if len(heap) > k:
    		heapq.heappop(heap)
    result = []
    while heap:
    	result.append(heapq.heappop(heap)[1])
    return result
#maintain a heap with size k here.
def topKFrequent(nums, k):
	count = Counter(nums)
	heap = []
	for num, freq in count.items():
		heapq.heappush(heap, (freq, num))
		if len(heapq) > k:
			heapq.heappop(heap)
	result = []
	while heap:
		result.append(heapq.heappop(heap)[1])
	return result

nums1 = [1,1,1,2,2,3]
k1 = 2

def topKFrequent(nums, k):
	count = Counter(nums)
	heap = []
	for num, freq in count.items():
		heapq.heappush(heap, (freq, num))
		if len(heap) > k:
			heapq.heappop(heap)
	result = []
	while heap:
		#add the value for that
		result.append(heapq.heappop(heap)[1])
	return result

def topKFrequent(nums, k):
	count = Counter(nums)
	heap = []
	for num, freq in count.items():
		heapq.heappush(heap, (freq, num))
		if len(heap) > k:
			heapq.heappop(heap)
	result = []
	while heap:
		result.append(heapq.heappop(heap)[1])
	return result


def topKFrequent(nums, k):
	count = Counter(nums)
	heap = []
	for num, freq in count.items():
		heapq.heappush(heap, (freq, num))
		if len(heap) > k:
			heapq.heappop(heap)
	result = []
	while heap:
		result.append(heapq.heappop(heap)[1])
	return result
#binary search:








