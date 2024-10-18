from collections.abc import Iterable


def deep_flatten(iterable):
    for item in iterable:
        if not isinstance(item, str) and isinstance(item, Iterable):
            yield from deep_flatten(item)
        else:
            yield item
