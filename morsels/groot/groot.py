from functools import wraps


def groot(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print('Groot')
    return inner
