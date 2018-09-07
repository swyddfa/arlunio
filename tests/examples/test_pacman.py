import matplotlib
import pytest
matplotlib.use("Agg")


def draw_pacman(width, height):

    # <example>

    import numpy as np

    from stylo.domain import SquareDomain
    from stylo.shape import Shape, Circle
    from stylo.color import FillColor, RGB8
    from stylo.image import SimpleImage

    class Pacman(Shape):

        def __init__(self, size, mouth):
            self.size = size
            self.mouth = mouth

        def draw(self):

            circle = Circle(0, 0, self.size)

            def pacman(x, y, t):
                in_circle = circle(x=x, y=y)
                not_in_mouth = np.abs(t) > (self.mouth * 0.6)

                return np.logical_and(in_circle, not_in_mouth)

            return pacman

    domain = SquareDomain(-1, 1)
    yellow = FillColor(RGB8.parse("ffff00"))
    img = SimpleImage(domain, Pacman(0.75, 1), yellow)

    # </example>

    img(width, height)

@pytest.mark.parametrize('n', [256, 1024, 4096])
def test_pacman(benchmark, n):
    benchmark(draw_pacman, n, n)
