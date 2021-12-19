import itertools
import math
import random

from .utils import CIRCUMFERENCE, Offset
from .extensions.LightshowTools import (
    _euclidean_distance,
    _color_merge,
    _color_from_distance,
)

HOT_COLORS = [
    (255, 0, 0),
    (255, 40, 0),
    (255, 80, 0),
    (255, 120, 0),
    (255, 160, 0),
    (255, 200, 0),
    (255, 255, 0),
]

COLD_COLORS = [
    (0, 0, 255),
    (0, 128, 255),
    (0, 255, 255),
    (128, 0, 255),
    (255, 0, 255),
]

TEST_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]


def fire(bottom, top, profile="h"):
    bottom = Offset(bottom, 3)
    top = Offset(top, 6)

    if profile == "h":
        colors, tfill, bfill = HOT_COLORS, (255, 20, 0), (255, 0, 0)
    elif profile == "c":
        colors, tfill, bfill = COLD_COLORS, (0, 0, 0), (0, 0, 0)

    bottom_points = (
        Point(bottom, i, *pos_from_center((0.5, 0.25), i, 0.4))
        for i in range(CIRCUMFERENCE)
    )

    top_points = (
        Point(top, i, *pos_from_center((0.5, 0.75), i, 0.4))
        for i in range(CIRCUMFERENCE)
    )

    points = list(itertools.chain(bottom_points, top_points))
    _test(bottom, top, points, profile)

    sparks = Sparks(colors)
    while True:
        bottom.fill(bfill)
        top.fill(tfill)
        for spark in sparks:
            spark.step(dx=0, dy=0.025)
        for point in points:
            point.update(sparks)
        bottom.show()
        top.show()
        sparks.prune()


def _test(bottom, top, points, profile):
    if not profile == "test":
        return
    collection = [
        Spark((255, 0, 0), 0.25, -0.5),
        Spark((0, 255, 0), 0.5, -0.5),
        Spark((0, 0, 255), 0.75, -0.5),
    ]
    sparks = Sparks(colors=TEST_COLORS, collection=collection)
    while True:
        bottom.fill((0, 0, 0))
        top.fill((0, 0, 0))
        for spark in sparks:
            spark.step(dx=0, dy=0.001)
        for point in points:
            point.update(sparks)
        bottom.show()
        top.show()


def pos_from_center(position, index, radius):
    angle = ((360 / CIRCUMFERENCE) * index) * (math.pi / 180)
    dy = radius * math.cos(angle)
    dx = radius * math.sin(angle)
    return (position[0] - dx, position[1] - dy)


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
        fan = self.fan
        index = self.index
        for spark in sparks:
            dist = _euclidean_distance(self.x, spark.x, self.y, spark.y)
            color = _color_from_distance(spark.color, dist, -20)
            fan[index] = _color_merge(fan[index], color)


class Spark(Coordinate):
    def __init__(self, color, x, y):
        super(Spark, self).__init__(x, y)
        self.color = color

    def step(self, dx, dy):
        self.x += dx
        self.y += dy


class Sparks:
    def __init__(self, colors, collection=None):
        self.colors = colors
        self.collection = collection or []

    def __iter__(self):
        for i in self.collection:
            yield i

    def prune(self):
        # remove sparks considered out of bounds
        self.collection = [
            c for c in self.collection if all(-0.5 < a < 1.5 for a in (c.y, c.x))
        ]

        if random.random() > 0.80 and len(self.collection) < 1000:
            self.collection.extend(
                [
                    Spark(random.choice(self.colors), random.random(), -0.5),
                    Spark(random.choice(self.colors), random.random(), -0.5),
                    Spark(random.choice(self.colors), random.random(), -0.5),
                ]
            )
