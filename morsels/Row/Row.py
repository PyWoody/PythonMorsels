class Row:

    def __init__(self, **data):
        self.__data = data

    def __repr__(self):
        cls = self.__class__.__name__
        kwargs = ', '.join(
            ('='.join((k, repr(v))) for k, v in self.__data.items())
        )
        return f'{cls}({kwargs})'

    def __dir__(self):
        return list(self.__data.keys())

    def __getattr__(self, name):
        try:
            return self.__data[name]
        except KeyError:
            raise AttributeError
