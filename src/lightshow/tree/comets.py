import itertools

from ..objects import Comet

def comet(pixels):
    comets = [
        Comet(0, -1, 10, (255, 0, 0), pixels),
        Comet(50, -1, 10, (0, 255, 0), pixels),
        Comet(100, -1, 10, (255, 0, 0), pixels),
        Comet(150, -1, 10, (0, 255, 0), pixels),
    ]
    for comet in itertools.cycle(comets):
        next(comet)