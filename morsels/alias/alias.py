class alias:

    def __init__(self, storage_name, write=False):
        self.storage_name = storage_name
        self.write = write

    def __set__(self, instance, value):
        if not self.write:
            raise AttributeError
        instance.__dict__[self.storage_name] = value

    def __get__(self, instance, owner):
        if instance is None:
            try:
                return owner.__dict__[self.storage_name]
            except KeyError:
                return self
        try:
            return instance.__dict__[self.storage_name]
        except KeyError:
            try:
                return instance.__getattribute__(self.storage_name)
            except AttributeError:
                return self


'''
class DataRecord:

    title = alias('serial', write=True)

    def __init__(self, serial):
        self.serial = serial


data = DataRecord('test')
data.serial
data.title
breakpoint()
'''
