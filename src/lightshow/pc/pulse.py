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

from .utils import DualColumn, Offset, SingleColumn, color_add

from ..tools import circle_indexes, color_maker


def pulse(px1, px2):
    span = 7
    px1 = Offset(px1, 3)
    px2 = Offset(px2, 12)
    col = SingleColumn(px1, px2)
    for i in itertools.cycle(col):
        indexes = circle_indexes(i, span, len(col))
        for count, index in enumerate(indexes, start=-1 * span):
            col[index] = (
                0,
                255 - abs(int(count / span * 255)),
                255 - abs(int(count / span * 255)),
            )
        col.show()
        time.sleep(0.05)


def dual_pulse(px1, px2):
    span = 3
    px1 = Offset(px1, 3)
    px2 = Offset(px2, 6)
    cols = DualColumn(px1, px2)
    for i in itertools.cycle(cols):
        lft_idx = circle_indexes(i, span, len(cols))
        rgt_idx = circle_indexes(i, span, len(cols), offset=6)
        cols.clear()
        for count, (l_i, r_i) in enumerate(zip(lft_idx, rgt_idx), start=-1 * span):
            cols.left[l_i] = color_add(cols.left[l_i], (0, 255 - abs(int(count / span * 255)), 0))
            cols.right[r_i] = color_add(cols.right[r_i], (0, 0, 255 - abs(int(count / span * 255))))
        cols.show()
        time.sleep(0.05)


def quad_pulse(px1, px2):
    span = 2
    px1 = Offset(px1, 3)
    px2 = Offset(px2, 6)
    cols = DualColumn(px1, px2)
    for i in itertools.cycle(cols):
        cols.clear()

        idxs = (
            circle_indexes(i, span, len(cols), offset=n)
            for n in range(0, 12, 3)
        )

        colors = (
            (255, 0, 0),
            (255, 118, 38),
            (255, 237, 38),
            (255, 255, 255)
        )

        cfuncs = (
            color_maker(c) for c in colors
        )

        for lft_idx, rgt_idx, lft_c, rgt_c in zip(idxs, idxs, cfuncs, cfuncs):
            for count, (l_i, r_i) in enumerate(zip(lft_idx, rgt_idx), start=-1 * span):
                cols.left[l_i] = color_add(cols.left[l_i], lft_c(count, span))
                cols.right[r_i] = color_add(cols.right[r_i], rgt_c(count, span))
        cols.show()
        time.sleep(0.10)