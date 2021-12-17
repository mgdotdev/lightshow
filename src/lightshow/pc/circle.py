import time
import itertools

PIXELS = 13

from ..tools import circle_indexes


def circle(px1, px2):
    for i in itertools.cycle(range(PIXELS)):
        span = 12
        _cyan = circle_indexes(i, span, PIXELS)
        for pixels in (px1, px2):
            for count, index in enumerate(_cyan, start=-1 * span):
                pixels[index] = (
                    0,
                    255 - abs(int(count / span * 255)),
                    255 - abs(int(count / span * 255)),
                )

        time.sleep(0.05)
        px1.show()
        px2.show()
