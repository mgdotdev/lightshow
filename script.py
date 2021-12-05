import itertools
import sys

import board
import neopixel
import time

PIXEL_COUNT = 50


def circle_indexes(center, spread, offset=0):
    return tuple(
        (i % PIXEL_COUNT)
        for i in range(center - spread + offset, center + spread + offset + 1)
    )


def circle(pixels):
    for i in itertools.cycle(range(PIXEL_COUNT)):
        span = 12
        _reds = circle_indexes(i, span)
        _greens = circle_indexes(i, span, offset=PIXEL_COUNT // 2)

        for count, index in enumerate(_reds, start=-1 * span):
            pixels[index] = (0, 255 - abs(int(count / span * 255)), 0)

        for count, index in enumerate(_greens, start=-1 * span):
            pixels[index] = (255 - abs(int(count / span * 255)), 0, 0)


class Comet:
    def __init__(self, start, step, length, color, pixels):
        self.current = start
        self.step = step
        self.pixels = pixels
        self.colors = [
            tuple((c - ((i / (length - 1)) * c)) for c in color) for i in range(length)
        ] + [(0, 0, 0)]

    def __iter__(self):
        return self

    def __next__(self):
        self.current = (self.current + self.step) % len(self.pixels)
        for idx, item in enumerate(self.colors):
            self.pixels[(self.current + idx) % len(self.pixels)] = item


def comets(pixels):
    comets = [
        Comet(0, -1, 10, (255, 0, 0), pixels),
        Comet(12, -1, 10, (0, 255, 0), pixels),
        Comet(25, -1, 10, (255, 0, 0), pixels),
        Comet(37, -1, 10, (0, 255, 0), pixels),
    ]
    for comet in itertools.cycle(comets):
        next(comet)
    time.sleep(0.1)


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


main()
