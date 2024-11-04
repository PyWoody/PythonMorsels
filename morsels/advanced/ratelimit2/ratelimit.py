import time

from functools import wraps


class ratelimit:

    def __init__(self, per_second, sleep=False):
        self.per_second = int(per_second)
        self.sleep = sleep
        self.attempts = []

    def __enter__(self):
        return self.attempt()

    def __exit__(self, *args, **kwargs):
        return False

    def __call__(self, func):

        @wraps(func)
        def inner(*args, **kwargs):
            self.attempt()
            return func(*args, **kwargs)

        return inner

    def attempt(self):
        now = time.perf_counter()
        if len(self.attempts) >= self.per_second:
            self.attempts = [
                i for i in self.attempts if now - i < 1.0
            ]
            if len(self.attempts) >= self.per_second:
                if self.sleep:
                    while len(self.attempts) >= self.per_second:
                        time.sleep(
                            min(1 - (now - i) for i in self.attempts)
                        )
                        now = time.perf_counter()
                        self.attempts = [
                            i for i in self.attempts if now - i < 1.0
                        ]
                else:
                    raise Exception
        self.attempts.append(now)
