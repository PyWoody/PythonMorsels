from collections.abc import Iterable
from functools import partial


__all__ = [
    'smoosh',
    'smooosh',
    'smoooosh',
    'smooooosh',
    'smoooooosh',
    'smooooooosh',
    'smoooooooosh',
    'smooooooooosh',
    'smoooooooooosh',
]


def __dir__():
    return __all__


def __getattr__(name):
    if name.startswith('smoo') and name.endswith('sh'):
        max_level = name.count('o') - 1
        return partial(smoosher, max_level)
    raise AttributeError


def smoosher(level, iterable):
    for item in iterable:
        if is_iterable(item) and level > 0:
            yield from smoosher(level - 1, item)
        else:
            yield item


def is_iterable(iterable):
    if isinstance(iterable, str):
        return False
    return True if isinstance(iterable, Iterable) else False
