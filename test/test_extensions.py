from lightshow.pc.extensions.LightshowTools import (
    _euclidean_distance,
    _color_merge,
    _color_from_distance,
)


class TestExtenstions:
    def test_euclidean_distance(self):
        assert _euclidean_distance(1, 1, 1, 2) == 1

    def test_color_merge(self):
        assert _color_merge([0, 0, 0], (0, 0, 0)) == (0, 0, 0)
        assert _color_merge([255, 255, 255], (255, 255, 255)) == (255, 255, 255)
        assert _color_merge([64, 64, 64], (64, 64, 64)) == (128, 128, 128)

    def test_color_from_distance(self):
        assert _color_from_distance((255, 255, 255), 0.01, -10) == (230, 230, 230)

    def test_color_from_distance(self):
        res = _color_from_distance((255, 255, 255), 1, -0.25)
        assert res
