from abc import ABC


class Iterable(ABC):

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Iterable:
            if any(
                hasattr(B, i)
                for B in C.__mro__
                for i in ('__iter__', '__getitem__')
            ):
                return True
        return NotImplemented


class Mapping(ABC):

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Mapping:
            members = ['keys', 'values', 'items', '__getitem__', '__iter__']
            for B in C.__mro__:
                if all(hasattr(B, i) for i in members):
                    return True
        return NotImplemented


class MetaHashable(type):

    def __instancecheck__(self, instance):
        try:
            _ = hash(instance)
        except TypeError:
            return False
        else:
            return True

    def __subclasscheck__(self, instance):
        for B in instance.__mro__:
            if '__hash__' in B.__dict__:
                if B.__dict__['__hash__'] is None:
                    return False
        return True


class Hashable(metaclass=MetaHashable):
    pass


class MetaImmutableSequence(type):

    def __instancecheck__(self, instance):
        if hasattr(instance, '__setitem__'):
            return False
        try:
            _ = hash(instance)
        except TypeError:
            return False
        else:
            return True

    def __subclasscheck__(self, instance):
        if hasattr(instance, '__setitem__') or issubclass(instance, set):
            return False
        return True


class ImmutableSequence(metaclass=MetaImmutableSequence):
    pass
