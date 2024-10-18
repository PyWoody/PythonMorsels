import functools


NO_RETURN = object()

def record_calls(func):

    @functools.wraps(func)
    def inner(*args, **kwargs):
        inner.call_count += 1
        try:
            return_value = func(*args, **kwargs)
        except Exception as e:
            inner.calls.append(Call(*args, **kwargs, exception=e))
            raise e
        else:
            inner.calls.append(
                Call(*args, **kwargs, return_value=return_value)
            )
            return return_value
    inner.call_count = 0
    inner.calls = []
    return inner


class Call:

    def __init__(
        self, *args, return_value=NO_RETURN, exception=None, **kwargs
    ):
        self.args = args
        self.kwargs = kwargs
        self.return_value = return_value
        self.exception = exception
