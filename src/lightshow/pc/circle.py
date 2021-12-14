import time
import itertools

PIXELS = 13

def circle_indexes(center, spread, pixel_count, offset=0):
    return tuple(
        (i % pixel_count)
        for i in range(center - spread + offset, center + spread + offset + 1)
    )


def circle(px1, px2):
    for i in itertools.cycle(range(PIXELS)):
        span = 12
        _cyan = circle_indexes(i, span, PIXELS)
        for pixels in (px1, px2):
            for count, index in enumerate(_cyan, start=-1 * span):
                pixels[index] = (0, 255 - abs(int(count / span * 255)), 255 - abs(int(count / span * 255)))

        time.sleep(0.05)
        px1.show()
        px2.show()
