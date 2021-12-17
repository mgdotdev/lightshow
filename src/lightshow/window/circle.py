import time
import itertools

from ..tools import circle_indexes, color_fader


def circle(pixels):
    pixel_count = len(pixels)
    cfuncs = [color_fader((0, 255, 0)), color_fader((255, 0, 0))]

    for i in itertools.cycle(range(pixel_count)):
        span = 12
        _reds = circle_indexes(i, span, pixel_count)
        _greens = circle_indexes(i, span, pixel_count, offset=pixel_count // 2)

        for count, index in enumerate(_reds, start=-1 * span):
            pixels[index] = cfuncs[0](count, span)

        for count, index in enumerate(_greens, start=-1 * span):
            pixels[index] = cfuncs[1](count, span)

        time.sleep(0.05)
        pixels.show()
