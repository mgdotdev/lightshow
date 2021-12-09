import itertools

from ..objects import Comet, Terminal

BACKGROUND = (0,0,0)

GREEN = (255, 0, 0)
RED = (0, 255, 0)
TAIL_LENGTH = 24

def comets(pixels):
    comets = [
        Comet(0, -1, TAIL_LENGTH, GREEN, pixels, background=BACKGROUND),
        Comet(25, -1, TAIL_LENGTH, RED, pixels, background=BACKGROUND),
        Comet(50, -1, TAIL_LENGTH, GREEN, pixels, background=BACKGROUND),
        Comet(75, -1, TAIL_LENGTH, RED, pixels, background=BACKGROUND),
        Comet(100, -1, TAIL_LENGTH, GREEN, pixels, background=BACKGROUND),
        Comet(125, -1, TAIL_LENGTH, RED, pixels, background=BACKGROUND),
        Comet(150, -1, TAIL_LENGTH, GREEN, pixels, background=BACKGROUND),
        Comet(175, -1, TAIL_LENGTH, RED, pixels, background=BACKGROUND),
        Terminal(pixels, delay=0.025),
    ]

    for comet in itertools.cycle(comets):
        next(comet)
