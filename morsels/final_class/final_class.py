class Unsubclassable:

    def __init_subclass__(self, *args, **kwargs):
        raise TypeError("type 'Unsubclassable' is not an acceptable base type")


def final_class(cls):
    def inner(*args, **kwargs):
        raise TypeError
    cls.__init_subclass__ = inner
    return cls


class UnsubclassableType(type):

    def __new__(meta_cls, cls_name, bases, cls_dict):
        return Unsubclassable
