import itertools
import time

from ..objects import Comet, Terminal
from ..pc.extensions.LightshowTools import (
    _color_merge,
    _color_from_distance,
)

BACKGROUND = (1, 1, 1)

PRIMARY = (255, 0, 0)
SECONDARY = (0, 255, 0)
TAIL_LENGTH = 10


def comets(pixels):
    comets = [
        Comet(0, 1, TAIL_LENGTH, PRIMARY, pixels, background=BACKGROUND),
        # Comet(25, 1, TAIL_LENGTH, SECONDARY, pixels, background=BACKGROUND),
        # Comet(50, 1, TAIL_LENGTH, PRIMARY, pixels, background=BACKGROUND),
        Comet(75, 1, TAIL_LENGTH, SECONDARY, pixels, background=BACKGROUND),
        # Comet(100, 1, TAIL_LENGTH, PRIMARY, pixels, background=BACKGROUND),
        # Comet(125, 1, TAIL_LENGTH, SECONDARY, pixels, background=BACKGROUND),
        Comet(150, 1, TAIL_LENGTH, PRIMARY, pixels, background=BACKGROUND),
        # Comet(175, 1, TAIL_LENGTH, SECONDARY, pixels, background=BACKGROUND),
        # Comet(200, 1, TAIL_LENGTH, PRIMARY, pixels, background=BACKGROUND),
        Comet(225, 1, TAIL_LENGTH, SECONDARY, pixels, background=BACKGROUND),
        # Comet(250, 1, TAIL_LENGTH, PRIMARY, pixels, background=BACKGROUND),
        # Comet(275, 1, TAIL_LENGTH, SECONDARY, pixels, background=BACKGROUND),
        Comet(300, 1, TAIL_LENGTH, PRIMARY, pixels, background=BACKGROUND),
        # Comet(225, 1, TAIL_LENGTH, SECONDARY, pixels, background=BACKGROUND),
        # Comet(250, 1, TAIL_LENGTH, PRIMARY, pixels, background=BACKGROUND),
        Terminal(pixels, delay=0.0125),
    ]

    for comet in itertools.cycle(comets):
        next(comet)


def _update_lights(pixels, sparks):
    for index, item in enumerate(pixels):
        for spark in sparks:
            dist = abs(spark.x - index)
            color = _color_from_distance(spark.color, dist, -20)
            pixels[index] = _color_merge(item, color)


class Spark:
    def __init__(self, x, color):
        self.x = x
        self.color = color

    def step(self, dx):
        self.x += dx


class Sparks:
    def __init__(self, *args):
        self.coll = list(args)

    def __iter__(self):
        return iter(self.coll)

    def add(self, *sparks):
        self.coll.extend(sparks)

    def step(self, dx):
        for spark in self.coll:
            spark.step(dx)

    def prune(self):
        self.coll = [
            item for item in self.coll if item.x > 400
        ]

    def replenish(self):
        if len(self.coll) < 1:
            self.add(Spark(-0.5, (255,0,0)))


def new_comets(pixels):
    sparks = Sparks()
    while True:
        pixels.fill((0,0,0))
        sparks.replenish()
        sparks.step(1)
        _update_lights(pixels, sparks)
        pixels.show()
        sparks.prune()
        time.sleep(0.05)
