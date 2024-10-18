from functools import partial


def call_later(func, *args, **kwargs):
    return partial(func, *args, **kwargs)
