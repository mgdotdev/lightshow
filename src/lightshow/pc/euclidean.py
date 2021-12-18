import itertools
import math
import time

from lightshow.pc.utils import CIRCUMFERENCE, Offset, color_add


def fire(bottom, top):
    bottom = Offset(bottom, 9)
    top = Offset(top, 6)

    bottom_points = (
        Point(bottom, i, *pos_from_center((0, 0.3), i, 0.1)) for i in range(CIRCUMFERENCE)
    )

    top_points = (
        Point(top, i, *pos_from_center((0, 0.7), i, 0.1)) for i in range(CIRCUMFERENCE)
    )

    points = list(itertools.chain(bottom_points, top_points))

    sparks = [Spark((100,100,100), 0.5, 0.0)]

    while True:
        bottom.clear()
        top.clear()
        for spark in sparks:
            spark.step(0, 0.001)
        for point in points:
            point.update(sparks)
        bottom.show()
        top.show()
        print("repeat")
        time.sleep(0.125)


def pos_from_center(position, index, radius):
    angle = ((360 / CIRCUMFERENCE) * index) * (math.pi / 180)
    dy = radius * math.cos(angle)
    dx = radius * math.sin(angle)
    return (position[0] - dx, position[1] - dy)


def color_from_distance(color, distance):
    """using an exponential decay function to calculate falloff"""
    return tuple(int(c * math.e**(-25*distance)) for c in color)


def euclidean_distance(point, spark):
    return math.sqrt((point.x - spark.x) ** 2 + (point.y - spark.y) ** 2)


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Point(Coordinate):
    def __init__(self, fan, index, x, y):
        super(Point, self).__init__(x, y)
        self.fan = fan
        self.index = index

    def update(self, sparks):
        for spark in sparks:
            dist = euclidean_distance(self, spark)
            color = color_from_distance(spark.color, dist)
            self.fan[self.index] = color_add(self.fan[self.index], color)
            print(f"DISTANCE: {dist}")
            print(f"   COLOR: {color}")


class Spark(Coordinate):
    def __init__(self, color, x, y):
        super(Spark, self).__init__(x, y)
        self.color = color

    def step(self, dx, dy):
        self.x += dx
        self.y += dy
        print(f"COORDINATES: {(self.x, self.y)}")
