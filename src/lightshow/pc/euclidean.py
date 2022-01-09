import itertools
import math
import random

import requests

from datetime import datetime

from .utils import CIRCUMFERENCE, Offset
from .extensions.LightshowTools import (
    _euclidean_distance,
    _color_merge,
    _color_from_distance,
)

WEIGHT = -20
INCREMENT = (0, 0.025)


def _test(points, profile):
    if not profile == "test":
        return
    collection = [
        Spark((0, 255, 0), 0.5, 0),
        Spark((255, 0, 0), 0.25, 0),
        Spark((0, 0, 255), 0.75, 0),
    ]
    sparks = Sparks(colors=None, collection=collection)
    dy = 0.002
    while True:
        if not all(-0.1 <= a <= 1.1 for c in sparks.collection for a in (c.y, c.x)):
            dy = -dy
        sparks.step(0, dy)
        _paint_canvas(sparks, points, weight=-30)


def _clock_hook_closure():
    def _clock_hook(sparks, points):
        now = datetime.now()
        if now.hour != _clock_hook.current.hour:
            _strike_on_hour(sparks, points, current=now)
            _clock_hook.current = now

    _clock_hook.current = datetime.now()
    return _clock_hook


def _strike_on_hour(sparks, points, current):
    _taper_sparks(sparks, points)

    weight = -9
    increment = (0, 0.0075)
    color = (255, 255, 255)

    appends = 0
    hour = current.hour
    
    if hour > 12:
        hour = hour - 12
    elif hour == 0:
        hour = 12

    while appends != hour:
        if all(c.y > 0.5 for c in sparks.collection):
            sparks.add(
                Spark(color, 0.5, -0.5),
                Spark(color, 0.25, -0.5),
                Spark(color, 0.75, -0.5),
            )
            appends += 1
        sparks.step(*increment)
        _paint_canvas(sparks, points, weight=weight)
        sparks.prune()
    _taper_sparks(sparks, points, increment=increment, weight=weight)


def _paint_canvas(sparks, points, weight=WEIGHT):
    points.clear_fans()
    for point in points:
        point.update(sparks, weight=weight)
    points.show_fans()


def _taper_sparks(sparks, points, increment=INCREMENT, weight=WEIGHT):
    while sparks.collection:
        sparks.step(*increment)
        _paint_canvas(sparks, points, weight=weight)
        sparks.prune()


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

    sparks = Sparks(colors)
    points = Points(
        fans=(bottom, top), collection=list(itertools.chain(bottom_points, top_points))
    )

    _test(points, profile)
    _clock_hook = _clock_hook_closure()

    while True:
        sparks.step(*INCREMENT)
        _paint_canvas(sparks, points)
        _clock_hook(sparks, points)
        sparks.update()


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
        lat, lng = ip["loc"].split(",")
        query = f"lat={lat}&lng{lng}&formatted=0"
        resp = requests.get(f"https://api.sunrise-sunset.org/json?{query}")
        return resp.json()

    def _colors_from_datetime(self):
        now = datetime.now()
        sunrise, sunset = self.sunrise_and_sunset(now)

        if sunrise <= now <= sunset:
            return random.choice(ColorProfile.HOT_COLORS)
        return random.choice(ColorProfile.COLD_COLORS)

    def sunrise_and_sunset(self, now=None):
        if now is None:
            now = datetime.now()

        if not hasattr(self, "_sunrise_and_sunset") or now.day != self.current.day:
            self.current = now
            _sunrise_and_sunset = ColorProfile._request_sunrise_and_sunset(self.ip)
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
        if self.profile == "c":
            return random.choice(ColorProfile.COLD_COLORS)
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

    def update(self, sparks, weight=WEIGHT):
        fan = self.fan
        index = self.index
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


class Points:
    def __init__(self, fans, collection=None):
        self.fans = fans
        self.collection = collection or []

    def __iter__(self):
        for item in self.collection:
            yield item

    def clear_fans(self):
        for fan in self.fans:
            fan.clear()

    def show_fans(self):
        for fan in self.fans:
            fan.show()


class Sparks:
    def __init__(self, colors, collection=None):
        self.colors = colors
        self.collection = collection or []

    def __iter__(self):
        for i in self.collection:
            yield i

    def __len__(self):
        return len(self.collection)

    def prune(self):
        self.collection = [
            c for c in self.collection if all(-0.5 <= a <= 1.5 for a in (c.y, c.x))
        ]

    def add(self, *args):
        self.collection.extend(args)

    def step(self, dx, dy):
        for spark in self.collection:
            spark.step(dx, dy)

    def replenish(self):
        select = self.colors.random_selection
        if random.random() > 0.80 and len(self) < 1000:
            self.add(
                Spark(select(), random.random(), -0.5),
                Spark(select(), random.random(), -0.5),
                Spark(select(), random.random(), -0.5),
            )

    def update(self):
        self.prune()
        self.replenish()
