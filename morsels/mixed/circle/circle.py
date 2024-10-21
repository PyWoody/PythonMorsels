import math


class Circle:

    def __init__(self, radius=1):
        if float(radius) < 0:
            raise ValueError('Radius cannot be negative')
        self.__radius = float(radius)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.radius})'

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        if float(value) < 0:
            raise ValueError('Radius cannot be negative')
        self.__radius = float(value)

    @property
    def diameter(self):
        return self.radius * 2

    @diameter.setter
    def diameter(self, value):
        self.radius = float(value) / 2

    @property
    def area(self):
        return math.pi * (self.radius**2)
