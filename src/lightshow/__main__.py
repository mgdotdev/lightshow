import socket
import sys

import board
import neopixel

from .pc.circle import circle as pc_circle
from .tree.comets import comets as tree_comets
from .window.circle import circle as window_circle
from .window.comets import comets as window_comets

OFF = "off"

def main():
    target = socket.gethostname()
    _, effect = sys.argv
    if target == "apple":
        pixels = neopixel.NeoPixel(board.D18, 50, brightness=1, auto_write=False)
        pixels.fill((0, 0, 0))
        if effect == OFF:
            return        
        elif effect == "comets":
            window_comets(pixels)
        elif effect == "circle":
            window_circle(pixels)
    elif target == "mud":
        pixels = neopixel.NeoPixel(board.D18, 300, brightness=1, auto_write=False)
        pixels.fill((0, 0, 0))
        if effect == OFF:
            return
        elif effect == "comets":
            tree_comets(pixels)
    elif target == "keylime":
        px1 = neopixel.NeoPixel(board.D18, 13, brightness=1, auto_write=False)
        px2 = neopixel.NeoPixel(board.D21, 13, brightness=1, auto_write=False)
        px1.fill((0,0,0))
        px2.fill((0,0,0))
        if effect == OFF:
            return
        elif effect == "circle":
            pc_circle(px1, px2)
