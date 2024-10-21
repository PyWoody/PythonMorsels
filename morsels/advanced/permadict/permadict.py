from collections import UserDict


class PermaDict(UserDict):

    def __init__(self, *args, silent=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.silent = silent

    def __setitem__(self, key, value):
        if self.data.get(key):
            if self.silent:
                return
            raise KeyError
        self.data[key] = value

    def update(self, iterable=None, force=False, **kwargs):
        if iterable is not None:
            if hasattr(iterable, 'keys'):
                for k, v in iterable.items():
                    if force:
                        super().__setitem__(k, v)
                    else:
                        self.__setitem__(k, v)
            else:
                for k, v in iterable:
                    if force:
                        super().__setitem__(k, v)
                    else:
                        self.__setitem__(k, v)
        for k, v in kwargs.items():
            if force:
                super().__setitem__(k, v)
            else:
                self.__setitem__(k, v)

    def force_set(self, key, value):
        super().__setitem__(key, value)
