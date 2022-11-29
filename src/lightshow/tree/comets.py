import itertools
import time

from ..objects import Comet, Terminal
from .extensions import _color_from_collection

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
        pixels[index] = _color_from_collection(
            index,
            item,
            sparks,
        )

class Spark:
    def __init__(self, x, color, weight):
        self.x = x
        self.color = color
        self.weight = weight

    def step(self, dx):
        self.x += dx


def params_picker():
    colors = [
        ((255,0,0), -0.15),
        ((0,255,0), -0.15),
        ((255,0,0), -0.15),
        ((255,255,255), -0.2),
        ((0,255,0), -0.15),
        ((255,0,0), -0.15),
        ((0,255,0), -0.15),
        ((255,255,255), -0.2),
    ]
    coll = itertools.cycle(colors)
    def color():
        return next(coll)
    return color

class Sparks:
    def __init__(self, *args):
        self.coll = list(args)
        self._last = time.time()
        self._params = params_picker()

    def __iter__(self):
        return iter(self.coll)

    def add(self, *sparks):
        self.coll.extend(sparks)

    def step(self, dx):
        for spark in self.coll:
            spark.step(dx)

    def prune(self):
        self.coll = [
            item for item in self.coll if item.x < 450
        ]

    def replenish(self):
        now = time.time()
        if now - self._last > 1:
            self._last = now
            self.add(Spark(-50, *self._params()))


def new_comets(pixels):
    sparks = Sparks(Spark(-50, (255, 255, 255), -0.2))
    while True:
        pixels.fill((0,0,0))
        sparks.step(0.5)
        _update_lights(pixels, sparks)
        pixels.show()
        sparks.replenish()
        sparks.prune()

