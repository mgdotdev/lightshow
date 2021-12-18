import itertools
import math
import random

from lightshow.pc.utils import CIRCUMFERENCE, Offset, color_add


def fire(bottom, top):
    bottom = Offset(bottom, 9)
    top = Offset(top, 6)

    bottom_points = (
        Point(bottom, i, *pos_from_center((0.5, 0.2), i, 0.1))
        for i in range(CIRCUMFERENCE)
    )

    top_points = (
        Point(top, i, *pos_from_center((0.5, 0.8), i, 0.1))
        for i in range(CIRCUMFERENCE)
    )

    points = list(itertools.chain(bottom_points, top_points))

    sparks = Sparks([Spark((255, 0, 0), 0.75, 1.0), Spark((0, 0, 255), 0.25, 1.0)])

    while True:
        bottom.clear()
        top.clear()
        for spark in sparks:
            spark.step(dx=0, dy=-0.001)
        for point in points:
            point.update(sparks)
        bottom.show()
        top.show()
        sparks.prune()


def pos_from_center(position, index, radius):
    angle = ((360 / CIRCUMFERENCE) * index) * (math.pi / 180)
    dy = radius * math.cos(angle)
    dx = radius * math.sin(angle)
    return (position[0] - dx, position[1] - dy)


def color_from_distance(color, distance):
    """using an exponential decay function to calculate falloff"""
    return tuple(int(c * math.e ** (-25 * distance)) for c in color)


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


class Spark(Coordinate):
    def __init__(self, color, x, y):
        super(Spark, self).__init__(x, y)
        self.color = color

    def step(self, dx, dy):
        self.x += dx
        self.y += dy


class Sparks:
    def __init__(self, collection) -> None:
        self.collection = collection

    def __iter__(self):
        for i in self.collection:
            yield i

    def prune(self):
        self.collection = [
            c for c in self.collection if all(-0.5 < a < 1.5 for a in (c.y, c.x))
        ]
        if random.random() > 0.95:
            self.collection.append(Spark((0, 255, 0), random.random(), 1.0))
        print([c.color for c in self.collection])
