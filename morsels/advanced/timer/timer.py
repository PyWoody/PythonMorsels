import heapq
import time


class Timer:

    def __init__(self, func=None):
        self.func = func
        self.elapsed = None
        self.runs = []
        self.start = None

    def __call__(self, *args, **kwargs):
        start = time.perf_counter()
        response = self.func(*args, **kwargs)
        self.elapsed = time.perf_counter() - start
        # heapq.heappush(self.runs, self.elapsed)
        self.runs.append(self.elapsed)
        return response

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed = time.perf_counter() - self.start
        # heapq.heappush(self.runs, self.elapsed)
        self.runs.append(self.elapsed)

    @property
    def min(self):
        return min(self.runs)

    @property
    def max(self):
        return max(self.runs)

    @property
    def median(self):
        pivot = len(self.runs) // 2
        self.runs.sort()
        if len(self.runs) % 2 == 0:
            return (self.runs[pivot - 1] + self.runs[pivot]) / 2
        return self.runs[pivot]

    @property
    def mean(self):
        return sum(self.runs) / len(self.runs)
