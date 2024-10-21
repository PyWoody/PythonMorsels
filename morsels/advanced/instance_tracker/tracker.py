import weakref


def instance_tracker(name='instances'):

    class InlineTrackerBase:

        instances = weakref.WeakSet()

        def __new__(cls, *args, **kwargs):
            new_cls = super().__new__(cls)
            InlineTrackerBase.instances.add(new_cls)
            return new_cls


    cls = InlineTrackerBase
    setattr(cls, name, InlineTrackerBase.instances)
    return cls
