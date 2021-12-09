import itertools

from ..objects import Comet

def comets(pixels):
    comets = [
        Comet(0, -1, 40, (255, 0, 0), pixels, background=(100,100,100)),
        Comet(50, -1, 40, (0, 255, 0), pixels, background=(100,100,100)),
        Comet(100, -1, 40, (255, 0, 0), pixels, background=(100,100,100)),
        Comet(150, -1, 40, (0, 255, 0), pixels, background=(100,100,100)),
    ]
    for comet in itertools.cycle(comets):
        next(comet)
