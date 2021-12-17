def circle_indexes(center, spread, pixel_count, offset=0):
    return tuple(
        (i % pixel_count)
        for i in range(center - spread + offset, center + spread + offset + 1)
    )


def color_maker(color):
    def maker(count, span):
        return tuple((c - abs(int(count / span * c))) for c in color)

    return maker
