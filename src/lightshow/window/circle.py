import time
import itertools

from ..tools import circle_indexes


def circle(pixels):
    pixel_count = len(pixels)
    for i in itertools.cycle(range(pixel_count)):
        span = 12
        _reds = circle_indexes(i, span, pixel_count)
        _greens = circle_indexes(i, span, pixel_count, offset=pixel_count // 2)

        for count, index in enumerate(_reds, start=-1 * span):
            pixels[index] = (0, 255 - abs(int(count / span * 255)), 0)

        for count, index in enumerate(_greens, start=-1 * span):
            pixels[index] = (255 - abs(int(count / span * 255)), 0, 0)

        time.sleep(0.05)
        pixels.show()
