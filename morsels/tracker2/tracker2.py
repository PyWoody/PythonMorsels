import weakref

def track_instances(cls=None, /, instance_name='instances'):
    _instances = weakref.WeakKeyDictionary()

    if isinstance(cls, str):
        instance_name = cls

    def wrapper(cls):

        def inner(*args, **kwargs):
            instance = cls(*args, **kwargs)
            setattr(instance, instance_name, _instances)
            _instances[instance] = None
            return instance

        setattr(inner, instance_name, _instances)
        return inner

    if isinstance(cls, type):
        return wrapper(cls)

    return wrapper
