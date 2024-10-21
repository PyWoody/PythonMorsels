import abc

from numbers import Number


class Validator(abc.ABC):

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        try:
            return instance.__dict__[self.storage_name]
        except KeyError:
            if self.value is not None:
                self.__set__(instance, self.value)
                return self.value
            cls = instance.__class__.__name__
            raise AttributeError(
                f"{cls!r} object has no attribute '{self.storage_name}'"
            )

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.storage_name] = value

    @abc.abstractmethod
    def validate(self, value):
        pass


class PositiveNumber(Validator):

    def __init__(self, value=None):
        self.value = value

    def validate(self, value):
        if not isinstance(value, Number):
            raise TypeError
        if value > 0:
            return value
        raise ValueError('Positive number required.')
