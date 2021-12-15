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


class SingleColumn:
    """Maps __setitem__ to the LEDs around the two column fans, reflected across
    x axis."""
    def __init__(self, bottom, top) -> None:
        self.top = top
        self.bottom = bottom

    def __setitem__(self, key, val):
        if key <= CIRCUMFERENCE // 2:
            target = self.bottom
        else:
            target = self.top
        target[key] = val
        target[CIRCUMFERENCE - key] = val

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