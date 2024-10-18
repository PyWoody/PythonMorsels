class Point:

    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, z={self.z})'

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        for s, o in zip(self, other):
            if s != o:
                return False
        return True

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(
                x=self.x + other.x, y=self.y + other.y, z=self.z + other.z
            )
        return Point(
            x=self.x + int(other),
            y=self.y + int(other),
            z=self.z + int(other),
        )

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(
                x=self.x - other.x, y=self.y - other.y, z=self.z - other.z
            )
        return Point(
            x=self.x - int(other),
            y=self.y - int(other),
            z=self.z - int(other),
        )

    def __div__(self, other):
        if isinstance(other, Point):
            return Point(
                x=self.x * other.x, y=self.y * other.y, z=self.z * other.z
            )
        return Point(
            x=self.x / int(other),
            y=self.y / int(other),
            z=self.z / int(other),
        )

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(
                x=self.x * other.x, y=self.y * other.y, z=self.z * other.z
            )
        return Point(
            x=self.x * int(other),
            y=self.y * int(other),
            z=self.z * int(other),
        )

    def __rmul__(self, other):
        if isinstance(other, Point):
            return Point(
                x=self.x * other.x, y=self.y * other.y, z=self.z * other.z
            )
        return Point(
            x=self.x * int(other),
            y=self.y * int(other),
            z=self.z * int(other),
        )
