from numbers import Number


class Vector:

    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}(x={self.x}, y={self.y}, z={self.z})'

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __setattr__(self, attr, value):
        # if attr in {'x', 'y', 'z'}:
        if attr in self.__slots__:
            try:
                super().__getattribute__(attr)
            except AttributeError:
                super().__setattr__(attr, value)
            else:
                raise Exception
        else:
            raise AttributeError('Vectors are immutable')

    def __eq__(self, other):
        try:
            return tuple(self) == tuple(other)
        except Exception:
            return False

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        raise TypeError

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        raise TypeError

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, Number):
            return Vector(self.x * other, self.y * other, self.z * other)
        raise TypeError

    __rmul__ = __mul__
