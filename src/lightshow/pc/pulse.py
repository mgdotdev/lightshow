"""
bottom fans, top pixel in circle is px1[10], bottom is px1[3]
top fans, top pixel in circle is px2[12], bottom is px2[6]
ascends counterclockwise

           12
         3    9
           6

           10
         0    7
           3
"""

import time
import itertools

CIRCUMFERENCE = 13

class Offset:
    """Allows us to pretend that the fan circle starts at zero at the bottom."""
    def __init__(self, px, offset) -> None:
        self.px = px
        self.offset = offset

    def __setitem__(self, key, val):
        new = (key + self.offset) % CIRCUMFERENCE
        self.px[new] = val

    def fill(self, *args, **kwargs):
        self.px.fill(*args, **kwargs)

    def show(self, *args, **kwargs):
        self.px.show(*args, **kwargs)


class Column:
    """Maps __setitem__ to the LEDs around the two column fans, reflected across
    x axis."""
    def __init__(self, bottom, top) -> None:
        self.top = top
        self.bottom = bottom

    def __setitem__(self, key, val):
        if key <= CIRCUMFERENCE // 2:
            self.bottom[key] = val
            self.bottom[CIRCUMFERENCE - key] = val
        else:
            self.top[key] = val
            self.top[CIRCUMFERENCE - key] = val

    def __len__(self):
        return CIRCUMFERENCE + 1

    def __iter__(self):
        for i in range(len(self)):
            yield i

    def fill(self):
        self.bottom.fill()
        self.top.fill()

    def show(self):
        self.bottom.show()
        self.top.show()


def pulse_indexes(center, spread, pixel_count, offset=0):
    return tuple(
        (i % pixel_count)
        for i in range(center - spread + offset, center + spread + offset + 1)
    )


def pulse(px1, px2):
    span = 7
    px1 = Offset(px1, 3)
    px2 = Offset(px2, 12)
    col = Column(px1, px2)
    for i in itertools.cycle(col):
        indexes = pulse_indexes(i, span, len(col))
        for count, index in enumerate(indexes, start=-1 * span):
            col[index] = (0, 255 - abs(int(count / span * 255)), 255 - abs(int(count / span * 255)))
        col.show()
        time.sleep(0.05)

