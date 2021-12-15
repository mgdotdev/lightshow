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

from .utils import Offset, SingleColumn

from ..tools import circle_indexes


def pulse(px1, px2):
    span = 7
    px1 = Offset(px1, 3)
    px2 = Offset(px2, 12)
    col = SingleColumn(px1, px2)
    for i in itertools.cycle(col):
        indexes = circle_indexes(i, span, len(col))
        for count, index in enumerate(indexes, start=-1 * span):
            col[index] = (0, 255 - abs(int(count / span * 255)), 255 - abs(int(count / span * 255)))
        col.show()
        time.sleep(0.05)

