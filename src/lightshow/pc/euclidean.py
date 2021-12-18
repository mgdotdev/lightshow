import itertools
import math

from lightshow.pc.utils import CIRCUMFERENCE, Offset, color_add


def fire(bottom, top):
    bottom = Offset(bottom, 3)
    top = Offset(top, 6)

    bottom_points = (
        Point(bottom, i, *pos_from_center(0.3, i, 0.1)) for i in range(CIRCUMFERENCE)
    )

    top_points = (
        Point(top, i, *pos_from_center(0.3, i, 0.1)) for i in range(CIRCUMFERENCE)
    )

    points = list(itertools.chain(bottom_points, top_points))

    sparks = [Spark((255, 255, 255), i / 10, 0) for i in range(-10, 10)]

    while True:
        for spark in sparks:
            spark.step(0.01, 0)
        for point in points:
            point.update(sparks)
        bottom.show()
        top.show()
        print("repeat")


def pos_from_center(position, index, radius):
    angle = ((360 / CIRCUMFERENCE) * index) * (math.pi / 180)
    dy = radius * math.cos(angle)
    dx = radius * math.sin(angle)
    return (position[0] - dx, position[1] - dy)


def color_from_distance(color, distance):
    return tuple(int(c * (1 / (distance * 25))) for c in color)


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
            self.fan[self.index] = color_add(self.point, color)


class Spark(Coordinate):
    def __init__(self, color, x, y):
        super(Point, self).__init__(x, y)
        self.color = color

    def step(self, dx, dy):
        self.x += dx
        self.y += dy
