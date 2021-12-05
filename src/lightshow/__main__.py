import sys

import board
import neopixel

from .window.circle import circle
from .window.comets import comets

PIXEL_COUNT = 50


def main():
    pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, brightness=1)
    pixels.fill((0, 0, 0))
    arg = sys.argv[-1]
    if arg == "off":
        return
    elif arg == "comets":
        comets(pixels)
    elif arg == "circle":
        circle(pixels)
