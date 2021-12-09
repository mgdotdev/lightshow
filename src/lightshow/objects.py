import time


class Comet:
    def __init__(self, start, step, length, color, pixels, background=(0, 0, 0)):
        self.current = start
        self.step = step
        self.pixels = pixels
        self.colors = [tuple(0.5 * c for c in color)]
        self.colors.extend([color, color])
        self.colors.extend(
            [
                tuple((c - ((i / (length - 1)) * c)) for c in color)
                for i in range(length - 3)
            ]
        )
        self.colors.append(background)

    def __iter__(self):
        return self

    def __next__(self):
        self.current = (self.current + self.step) % len(self.pixels)
        for idx, item in enumerate(self.colors):
            self.pixels[(self.current + idx) % len(self.pixels)] = item


class Terminal:
    def __init__(self, pixels, delay=0.01):
        self.pixels = pixels
        self.delay = delay

    def __iter__(self):
        return self

    def __next__(self):
        time.sleep(self.delay)
        self.pixels.show()
