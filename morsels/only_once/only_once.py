from functools import wraps

def only_once(func):
    fail = False

    @wraps(func)
    def inner(*args, **kwargs):
        nonlocal fail
        if fail:
            raise ValueError("You can't call this function twice!")
        fail = True
        return func(*args, **kwargs)
    return inner
