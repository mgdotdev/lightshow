import sys

import board
import neopixel

from .window.circle import circle as window_circle
from .window.comets import comets as window_comets
from .tree.comets import comets as tree_comets


def main():
    if sys.argv[-1] == "off":
        pixels = neopixel.NeoPixel(board.D18, 1000)
        pixels.fill((0, 0, 0))
        return
    _, target, effect = sys.argv
    if target == "window":
        pixels = neopixel.NeoPixel(board.D18, 50, brightness=1, auto_write=False)
        pixels.fill((0, 0, 0))
        if effect == "comets":
            window_comets(pixels)
        elif effect == "circle":
            window_circle(pixels)
    elif target == "tree":
        pixels = neopixel.NeoPixel(board.D18, 250, brightness=1, auto_write=False)
        pixels.fill((0, 0, 0))
        if effect == "comets":
            tree_comets(pixels)
