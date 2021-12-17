import time
import itertools

PIXELS = 13

from ..tools import circle_indexes, color_fader


def circle(px1, px2, color):
    cfunc = color_fader(color)
    for i in itertools.cycle(range(PIXELS)):
        span = 12
        _cyan = circle_indexes(i, span, PIXELS)
        for pixels in (px1, px2):
            for count, index in enumerate(_cyan, start=-1 * span):
                pixels[index] = cfunc(count, span)

        time.sleep(0.05)
        px1.show()
        px2.show()
