import itertools
import math
import random

import requests

from datetime import datetime

from .utils import CIRCUMFERENCE, Offset, SingleColumn
from .extensions.LightshowTools import (
    _euclidean_distance,
    _color_merge,
    _color_from_distance,
)

from ..tools import circle_indexes, color_fader

WEIGHT = -20


def _test(bottom, top, points, profile):
    if not profile == "test":
        return
    collection = [
        Spark((0, 255, 0), 0.5, 0),
        Spark((255, 0, 0), 0.25, 0),
        Spark((0, 0, 255), 0.75, 0),
    ]
    sparks = Sparks(colors=None, collection=collection)
    for point in points:
        point.weight = -30
    dy = 0.002
    while True:
        bottom.clear()
        top.clear()
        if not all(-0.1 <= a <= 1.1 for c in sparks.collection for a in (c.y, c.x)):
            dy = -dy
        for spark in sparks:
            spark.step(dx=0, dy=dy)
        for point in points:
            point.update(sparks)
        bottom.show()
        top.show()


def _clock_hook_closure():
    def _clock_hook(sparks, points):
        now = datetime.now()
        hour = now.hour
        # if hour != _clock_hook.current.hour:
        _strike_on_hour(sparks, points, hour)
        _clock_hook.current = now
    _clock_hook.current = datetime.now()
    return _clock_hook


def _strike_on_hour(sparks, points, hour):
    _taper_sparks(sparks, points)
    for _ in range(hour):
        sparks.collection = [
            Spark((255, 255, 255), 0.5, -0.2),
            Spark((255, 255, 255), 0.25, -0.2),
            Spark((255, 255, 255), 0.75, -0.2),
        ]
        _taper_sparks(sparks, points)
        

def _taper_sparks(sparks, points):
    fans = set(p.fan for p in points)
    while sparks.collection:
        for fan in fans:
            fan.clear()
        for spark in sparks:
            spark.step(dx=0, dy=0.025)
        for point in points:
            point.update(sparks)
        sparks.collection = _pruned_collection(sparks.collection)
        for fan in fans:
            fan.show()


def _pruned_collection(collection):
    return [
        c for c in collection if all(-0.2 <= a <= 1.2 for a in (c.y, c.x))
    ]


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
    sparks = Sparks(colors)

    _test(bottom, top, points, profile)
    _clock_hook = _clock_hook_closure()

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

        _clock_hook(sparks, points)


def pos_from_center(position, index, radius):
    angle = ((360 / CIRCUMFERENCE) * index) * (math.pi / 180)
    dy = radius * math.cos(angle)
    dx = radius * math.sin(angle)
    return (position[0] - dx, position[1] - dy)


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
    def _request_sunrise_and_sunset(ip):
        loc = ip["loc"].split(",")
        return requests.get(
            "https://api.sunrise-sunset.org/json?lat={}&lng{}&formatted=0".format(*loc)
        ).json()

    def _colors_from_datetime(self):
        now = datetime.now()
        sunrise, sunset = self.sunrise_and_sunset(now)

        if sunrise <= now <= sunset:
            return random.choice(ColorProfile.HOT_COLORS)
        else:
            return random.choice(ColorProfile.COLD_COLORS)

    def sunrise_and_sunset(self, now=None):
        if now is None:
            now = datetime.now()

        if (
            not hasattr(self, "_sunrise_and_sunset")
            or now.day != self.current.day
        ):
            self.current = now
            _sunrise_and_sunset = ColorProfile._request_sunrise_and_sunset(
                self.ip
            )
            sunrise = _sunrise_and_sunset["results"]["sunrise"][:-6]
            sunset = _sunrise_and_sunset["results"]["sunset"][:-6]
            self._sunrise_and_sunset = (
                datetime.fromisoformat(sunrise),
                datetime.fromisoformat(sunset),
            )
        return self._sunrise_and_sunset

    def random_selection(self):
        if self.profile == "h":
            return random.choice(ColorProfile.HOT_COLORS)
        elif self.profile == "c":
            return random.choice(ColorProfile.COLD_COLORS)
        else:
            return self._colors_from_datetime()


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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
        self.collection = _pruned_collection(self.collection)

        if random.random() > 0.80 and len(self.collection) < 1000:
            self.collection.extend(
                [
                    Spark(self.colors.random_selection(), random.random(), -0.5),
                    Spark(self.colors.random_selection(), random.random(), -0.5),
                    Spark(self.colors.random_selection(), random.random(), -0.5),
                ]
            )
