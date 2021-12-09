import itertools

from ..objects import Comet, Terminal


def comets(pixels):
    comets = [
        Comet(0, -1, 10, (255, 0, 0), pixels),
        Comet(12, -1, 10, (0, 255, 0), pixels),
        Comet(25, -1, 10, (255, 0, 0), pixels),
        Comet(37, -1, 10, (0, 255, 0), pixels),
        Terminal(pixels, delay=0.1),
    ]
    for comet in itertools.cycle(comets):
        next(comet)
