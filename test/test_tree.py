from lightshow.tree.comets import Spark, Sparks
from lightshow.tree.extensions import _color_from_collection

class TestComets:
    def test_comets(self):
        sparks = Sparks(Spark(100, (255,255,255)))
        item = _color_from_collection(
            100,
            [0,0,0],
            sparks,
            -0.2
        )
        assert item == (255, 255, 255)


        item = _color_from_collection(
            50,
            [0,0,0],
            sparks,
            -0.2
        )
        assert item == (0, 0, 0)

        item = _color_from_collection(
            99,
            [0,0,0],
            sparks,
            -0.2
        )
        assert item == (208, 208, 208)
