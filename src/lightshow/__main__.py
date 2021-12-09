import sys

import board
import neopixel

from .window.circle import circle as window_circle
from .window.comets import comets as window_comets
from .tree.comets import comets as tree_comets

PIXEL_COUNT = 50

def main():
    pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, brightness=1)
    pixels.fill((0, 0, 0))
    if sys.argv[-1] == "off":
        return
    _, target, effect = sys.argv
    if target == "window":
        if effect == "comets":
            window_comets(pixels)
        elif effect == "circle":
            window_circle(pixels)
    elif target == "tree":
        if effect == "comets":
            tree_comets(pixels)
