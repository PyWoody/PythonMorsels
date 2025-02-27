import re
import unittest


SNAKE_RE = re.compile(r'[a-z]_[a-z]', re.IGNORECASE)
CAMEL_RE = re.compile(r'[a-z][A-Z]')
TO_SNAKE_RE = re.compile(r'[A-Z]')
TO_CAMEL_RE = re.compile(r'_([a-z])', re.IGNORECASE)
DUNDER_RE = re.compile(r'__.*__')


class SnakeTestCase(unittest.TestCase):

    def __init_subclass__(subclass):
        super().__init_subclass__()
        sentinel = object()
        for attr in dir(subclass):
            if is_camel(attr):
                snake_attr = getattr(subclass, to_snake(attr), sentinel)
                if snake_attr is not sentinel:
                    setattr(subclass, attr, snake_attr)

    def __getattribute__(self, key):
        if is_dunder(key):
            return super().__getattribute__(key)
        try:
            return super().__getattribute__(to_snake(key))
        except AttributeError:
            try:
                return super().__getattribute__(key)
            except AttributeError:
                return super().__getattribute__(to_camel(key))


class SnakeCaseMixin:

    def __getattribute__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            if is_dunder(key):
                raise AttributeError
            return super().__getattribute__(to_camel(key))


def allow_snake(cls):

    def __getattribute__(self, key):
        if is_dunder(key):
            return super(cls, self).__getattribute__(key)
        try:
            return super(cls, self).__getattribute__(to_snake(key))
        except AttributeError:
            try:
                return super(cls, self).__getattribute__(key)
            except AttributeError:
                return super(cls, self).__getattribute__(to_camel(key))

    cls.__getattribute__ = __getattribute__
    sentinel = object()
    for attr in dir(cls):
        if is_camel(attr):
            snake_attr = getattr(cls, to_snake(attr), sentinel)
            if snake_attr is not sentinel:
                setattr(cls, attr, snake_attr)
    return cls


def is_snake(item):
    if is_dunder(item):
        return False
    return bool(SNAKE_RE.search(str(item)))


def is_camel(item):
    if is_dunder(item):
        return False
    return bool(CAMEL_RE.search(str(item)))


def to_snake(item):
    def to_lower(matchobj):
        return f'_{matchobj.group(0).lower()}'
    return TO_SNAKE_RE.sub(to_lower, item)


def to_camel(item):
    def to_upper(matchobj):
        return matchobj.group(1).upper()
    return TO_CAMEL_RE.sub(to_upper, item)


def is_dunder(item):
    return bool(DUNDER_RE.fullmatch(item))
