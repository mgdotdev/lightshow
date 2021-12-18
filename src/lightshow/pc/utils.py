CIRCUMFERENCE = 13


def color_add(target, item):
    return tuple(
        int(i) if (i := sum((a, b))) < 255 else 255 for (a, b) in zip(target, item)
    )


class Offset:
    """Allows us to pretend that the fan circle starts at zero at the bottom."""

    def __init__(self, px, offset):
        self.px = px
        self.offset = offset

    def __setitem__(self, key, val):
        new = (key + self.offset) % CIRCUMFERENCE
        self.px[new] = val

    def __getitem__(self, key):
        new = (key + self.offset) % CIRCUMFERENCE
        return self.px[new]

    def clear(self):
        self.fill((0, 0, 0))

    def fill(self, *args, **kwargs):
        self.px.fill(*args, **kwargs)

    def show(self, *args, **kwargs):
        self.px.show(*args, **kwargs)


class ColumnUtil:
    def __init__(self, bottom, top):
        self.top = top
        self.bottom = bottom

    def __len__(self):
        return CIRCUMFERENCE + 1

    def __iter__(self):
        for i in range(len(self)):
            yield i

    def fill(self, val):
        self.bottom.fill(val)
        self.top.fill(val)

    def show(self):
        self.bottom.show()
        self.top.show()

    def clear(self):
        self.fill((0, 0, 0))


class SplitColumnUtil(ColumnUtil):
    def fill(self, val):
        for i in self:
            self[i] = val
        self.show()


class SingleColumn(ColumnUtil):
    """Maps __setitem__ to the LEDs around the two column fans, reflected across
    x axis."""

    def __setitem__(self, key, val):
        target = self._get_target(key)
        target[key] = val
        target[CIRCUMFERENCE - key] = val

    def __getitem__(self, key):
        target = self._get_target(key)
        return target[key]

    def _get_target(self, key):
        if key <= CIRCUMFERENCE // 2:
            target = self.bottom
        else:
            target = self.top
        return target


class LeftColumn(SplitColumnUtil):
    def __init__(self, bottom, top):
        super().__init__(bottom, top)

    def __setitem__(self, key, val):
        key, target = self._key_and_target(key)
        target[key] = val

    def __getitem__(self, key):
        key, target = self._key_and_target(key)
        return target[key]

    def _key_and_target(self, key):
        if key <= CIRCUMFERENCE // 2:
            target = self.bottom
            key = CIRCUMFERENCE - key
        else:
            target = self.top
            key = CIRCUMFERENCE + (CIRCUMFERENCE // 2) - key
        return key, target


class RightColumn(SplitColumnUtil):
    def __init__(self, bottom, top):
        super().__init__(bottom, top)

    def __setitem__(self, key, val):
        key, target = self._key_and_target(key)
        target[key] = val

    def __getitem__(self, key):
        key, target = self._key_and_target(key)
        return target[key]

    def _key_and_target(self, key):
        if key <= CIRCUMFERENCE // 2:
            target = self.bottom
        else:
            target = self.top
            key = key + (CIRCUMFERENCE // 2)
        return key, target


class DualColumn(ColumnUtil):
    def __init__(self, bottom, top):
        super().__init__(bottom, top)
        self.left = LeftColumn(bottom, top)
        self.right = RightColumn(bottom, top)
