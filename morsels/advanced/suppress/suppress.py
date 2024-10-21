from functools import wraps


class suppress:

    def __init__(self, *exceptions):
        self.exceptions = tuple(i for i in exceptions)
        self.exception = None
        self.traceback = None

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return inner

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            if exc_type in self.exceptions:
                self.exception = exc_value
                self.traceback = traceback
                return True
            elif issubclass(exc_type, self.exceptions):
                self.exception = exc_value
                self.traceback = traceback
                return True
