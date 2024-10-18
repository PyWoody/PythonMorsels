from math import tau


class NoSoupForYou:

    def __getitem__(self, *args, **kwargs):
        raise ImportError("Don't user import *")


__all__ = NoSoupForYou()
