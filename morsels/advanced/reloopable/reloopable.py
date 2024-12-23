class reloopable:

    instances = []

    def __init__(self, fobj, instance=None, stale=True, strict=False):
        self.fobj = fobj
        self.cur_instance = instance
        self.stale = bool(stale)
        self.strict = bool(strict)

    def __iter__(self):
        self.fobj.seek(0)
        self.cur_instance = object()
        self.instances.append(self.cur_instance)
        return type(self)(
            self.fobj, self.cur_instance, strict=self.strict, stale=self.stale
        )

    def __next__(self):
        if self.stale and self.cur_instance is not self.instances[-1]:
            if self.strict:
                raise RuntimeError
            raise StopIteration
        elif data := self.fobj.readline():
            return data
        else:
            raise StopIteration

    def __enter__(self, *args, **kwargs):
        return type(self)(self.fobj, stale=False)

    def __exit__(self, *args, **kwargs):
        self.fobj.close()
