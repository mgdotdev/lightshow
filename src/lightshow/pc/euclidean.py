import itertools
import math
import random

import requests

from datetime import datetime
from zoneinfo import ZoneInfo

from .utils import CIRCUMFERENCE, Offset
from .extensions.LightshowTools import (
    _euclidean_distance,
    _color_merge,
    _color_from_distance,
)

WEIGHT = -20


def _test(bottom, top, points, profile):
    if not profile == "test":
        return
    collection = [
        Spark((0, 255, 0), 0.5, -0.5),
        Spark((255, 0, 0), 0.25, -0.5),
        Spark((0, 0, 255), 0.75, -0.5),
    ]
    sparks = Sparks(colors=None, collection=collection)
    while True:
        bottom.clear()
        top.clear()
        for spark in sparks:
            spark.step(dx=0, dy=0.001)
        for point in points:
            point.weight = -30
            point.update(sparks)
        bottom.show()
        top.show()


def fire(bottom, top, profile=None):
    bottom = Offset(bottom, 3)
    top = Offset(top, 6)

    colors = ColorProfile(profile)

    bottom_points = (
        Point(bottom, i, *pos_from_center((0.5, 0.25), i, 0.2))
        for i in range(CIRCUMFERENCE)
    )

    top_points = (
        Point(top, i, *pos_from_center((0.5, 0.75), i, 0.2))
        for i in range(CIRCUMFERENCE)
    )

    points = list(itertools.chain(bottom_points, top_points))
    _test(bottom, top, points, profile)

    sparks = Sparks(colors)
    while True:
        bottom.clear()
        top.clear()
        for spark in sparks:
            spark.step(dx=0, dy=0.025)
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


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ColorProfile:
    HOT_COLORS = [
        (255, 0, 0),
        (255, 5, 0),
        (255, 10, 0),
        (255, 20, 0),
        (255, 40, 0),
        (255, 80, 0),
        (255, 120, 0),
        (255, 160, 0),
    ]

    COLD_COLORS = [
        (0, 0, 255),
        (0, 128, 255),
        (0, 255, 255),
        (128, 0, 255),
        (255, 0, 255),
    ]

    def __init__(self, profile):
        self.profile = profile
        self.current = datetime.now()
        self.ip = requests.get("https://ipinfo.io").json()

    @staticmethod
    def _request_metadata(ip):
        loc = ip["loc"].split(",")
        return requests.get(
            "https://api.sunrise-sunset.org/json?lat={}&lng{}&formatted=0".format(*loc)
        ).json()

    @property
    def metadata(self):
        if not hasattr(self, "_metadata"):
            self.current = datetime.now()
            _metadata = ColorProfile._request_metadata(self.ip)
            self._metadata = (
                datetime.fromisoformat(_metadata["results"]["sunrise"][:-6]),
                datetime.fromisoformat(_metadata["results"]["sunset"][:-6]),
            )
        elif (datetime.now() - self.current).days >= 1:
            self.current = datetime.now()
            _metadata = ColorProfile._request_metadata(self.ip)
            self._metadata = (
                datetime.fromisoformat(_metadata["results"]["sunrise"][:-6]),
                datetime.fromisoformat(_metadata["results"]["sunset"][:-6]),
            )
        return self._metadata

    def random_selection(self):
        if self.profile == "h":
            return random.choice(ColorProfile.HOT_COLORS)
        elif self.profile == "c":
            return random.choice(ColorProfile.COLD_COLORS)
        else:
            return self._colors_from_datetime()

    def _colors_from_datetime(self):
        sunrise, sunset = self.metadata
        now = datetime.now()
        if sunrise <= now <= sunset:
            return random.choice(ColorProfile.HOT_COLORS)
        return random.choice(ColorProfile.COLD_COLORS)


class Point(Coordinate):
    def __init__(self, fan, index, x, y):
        super(Point, self).__init__(x, y)
        self.fan = fan
        self.index = index
        self.weight = WEIGHT

    def update(self, sparks):
        fan = self.fan
        index = self.index
        weight = self.weight
        for spark in sparks:
            dist = _euclidean_distance(self.x, self.y, spark.x, spark.y)
            color = _color_from_distance(spark.color, dist, weight)
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
                    Spark(self.colors.random_selection(), random.random(), -0.5),
                    Spark(self.colors.random_selection(), random.random(), -0.5),
                    Spark(self.colors.random_selection(), random.random(), -0.5),
                ]
            )
