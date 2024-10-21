import functools
import time

from threading import Lock


def ratelimit(per_second=3, sleep=False):
    attempts = []
    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            now = time.perf_counter()
            if len(attempts) >= per_second:
                for i in range(len(attempts), 0 , -1):
                    if (now - attempts[i - 1]) > 1.0:
                        _ = attempts.pop(i - 1)
                if len(attempts) >= per_second:
                    if sleep:
                        time.sleep(min(attempts))
                    else:
                        raise Exception
            attempts.append(now)
            return func(*args, **kwargs)
        inner.attempts = attempts
        inner.per_second = per_second
        return inner
    return outer
