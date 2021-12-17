import socket
import sys

import board
from lightshow.tools import color_from_string
import neopixel


from .pc.circle import circle as pc_circle
from .tree.comets import comets as tree_comets
from .window.circle import circle as window_circle
from .window.comets import comets as window_comets
from .pc.pulse import (
    pulse as pc_pulse,
    dual_pulse as pc_dual_pulse,
    quad_pulse as pc_quad_pulse,
)

OFF = "off"


def main():
    target = socket.gethostname()
    _, effect, *options = sys.argv
    if target == "apple":
        pixels = neopixel.NeoPixel(board.D18, 50, brightness=1, auto_write=False)
        pixels.fill((0, 0, 0))
        pixels.show()
        if effect == OFF:
            return
        elif effect == "comets":
            window_comets(pixels)
        elif effect == "circle":
            window_circle(pixels)
    elif target == "mud":
        pixels = neopixel.NeoPixel(board.D18, 300, brightness=1, auto_write=False)
        pixels.fill((0, 0, 0))
        pixels.show()
        if effect == OFF:
            return
        elif effect == "comets":
            tree_comets(pixels)
    elif target == "keylime":
        px1 = neopixel.NeoPixel(board.D18, 13, brightness=1, auto_write=False)
        px2 = neopixel.NeoPixel(board.D21, 13, brightness=1, auto_write=False)
        for pixels in (px1, px2):
            pixels.fill((0, 0, 0))
            pixels.show()
        if effect == OFF:
            return
        elif effect == "circle":
            if options:
                color_string, = options
            else:
                color_string = "0,255,255"
            pc_circle(px1, px2, color_from_string(color_string))
        elif effect == "pulse":
            pc_pulse(px1, px2)
        elif effect == "dpulse":
            pc_dual_pulse(px1, px2)
        elif effect == "qpulse":
            pc_quad_pulse(px1, px2)
