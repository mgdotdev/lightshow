import sys

import board
import neopixel

from .window.circle import circle as window_circle
from .window.comets import comets as window_comets
from .tree.comets import comets as tree_comets

def main():
    if sys.argv[-1] == "off":
        return
    _, target, effect = sys.argv
    if target == "window":
        pixels = neopixel.NeoPixel(board.D18, 50, brightness=1)
        pixels.fill((0, 0, 0))
        if effect == "comets":
            window_comets(pixels)
        elif effect == "circle":
            window_circle(pixels)
    elif target == "tree":
        pixels = neopixel.NeoPixel(board.D18, 200, brightness=1)
        pixels.fill((0, 0, 0))
        if effect == "comets":
            tree_comets(pixels)
