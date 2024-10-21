import heapq


class BaseHeap:

    def __init__(self, items, key=None):
        self.key = key if key is not None else psuedo_key
        self.heap = [(self.key(i), i) for i in items]
        heapq.heapify(self.heap)

    def __len__(self):
        return len(self.heap)

    def push(self, item):
        return heapq.heappush(self.heap, (self.key(item), item))


class MinHeap(BaseHeap):

    def peek(self):
        return min(self.heap)[1]

    def pop(self):
        return heapq.heappop(self.heap)[1]


class MaxHeap(BaseHeap):

    def peek(self):
        return max(self.heap)[1]

    def pop(self):
        item = max(self.heap)
        self.heap.remove(item)
        return item[1]


def psuedo_key(item):
    return item
