import time

from contextlib import contextmanager


TIMERS = dict()


class Timer:

    def __init__(self, name=None):
        self.elapsed = None
        self.last_start = None
        self.runs = []
        self.splits = {}

    def __new__(meta_cls, name=None):
        if name is not None:
            if timer := TIMERS.get(name):
                return timer
        new_cls = super().__new__(meta_cls)
        TIMERS[name] = new_cls
        return new_cls

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({self.runs!r})'

    def __enter__(self):
        self.last_start = time.perf_counter()
        return self

    def __exit__(self, *args, **kwargs):
        self.elapsed = time.perf_counter() - self.last_start
        self.runs.append(self.elapsed)
        self.last_start = None

    def __getitem__(self, index):
        return self.splits[index]

    @contextmanager
    def split(self, name=None):
        if self.last_start is None:
            raise RuntimeError(
                'Cannot split because parent timer is not running'
            )
        if name is None:
            name = len(self.splits)
        with Timer() as sub_timer:
            sub_timer.split_name = name
            yield sub_timer
        if not self.splits.get(name):
            self.splits[name] = sub_timer
        else:
            self.splits[name].runs.append(sub_timer.elapsed)
