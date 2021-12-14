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
import random

CIRCUMFERENCE = 13

class Offset:
    def __init__(self, px, offset) -> None:
        self.px = px
        self.offset = offset

    def __setitem__(self, key, val):
        new = (key + self.offset) % CIRCUMFERENCE
        self.px[new] = val
        print(new)

    def fill(self, *args, **kwargs):
        self.px.fill(*args, **kwargs)

    def show(self, *args, **kwargs):
        self.px.show(*args, **kwargs)


class Column:
    """Maps items to the LEDs"""
    def __init__(self, bottom, top) -> None:
        self.top = top
        self.bottom = bottom

    def __setitem__(self, key, val):
        if key <= (CIRCUMFERENCE // 2) + 1:
            self.bottom[key] = val
            self.bottom[CIRCUMFERENCE - key] = val
        else:
            self.top[key] = val
            self.top[CIRCUMFERENCE - key] = val

    def show(self):
        self.bottom.show()
        self.top.show()
        

def pulse(px1, px2):
    px1 = Offset(px1, 3)
    px2 = Offset(px2, 12)
    col = Column(px1, px2)
    for i in itertools.cycle(range(CIRCUMFERENCE)):
        col[i] = tuple(random.randint(0,255) for _ in range(3))
        col.show()
        time.sleep(0.5)

