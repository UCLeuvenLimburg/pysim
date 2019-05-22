from __future__ import annotations


class Vector:
    __x : int
    __y : int

    def __init__(self, x : int, y : int):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def __add__(self, other : Vector) -> Vector:
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __neg__(self) -> Vector:
        x = -self.x
        y = -self.y
        return Vector(x, y)

    def __sub__(self, other : Vector) -> Vector:
        return self + -other

    def __mul__(self, factor : int) -> Vector:
        x = self.x * factor
        y = self.y * factor
        return Vector(x, y)


NORTH = Vector(0, -1)

EAST = Vector(1, 0)

SOUTH = Vector(0, 1)

WEST = Vector(-1, 0)
