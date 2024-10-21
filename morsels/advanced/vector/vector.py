class Vector:

    __slots__ = ('__x', '__y', '__z')

    def __init__(self, x, y, z):
        self.__x = int(x)
        self.__y = int(y)
        self.__z = int(z)

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __eq__(self, other):
        if isinstance(other, Vector):
            return list(self) == list(other)
        return False

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError
        return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError
        return Vector(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError
        return Vector(self.x / other, self.y / other, self.z / other)

    def __rtruediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError
        return Vector(self.x / other, self.y / other, self.z / other)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z
