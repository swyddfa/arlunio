"""
In this example we show how pacman can be drawn by defining your own custom
:code:`Shape` class. Building on the built in :code:`Circle` shape the definition is
quite simple as long as we remember that the :code:`in_circle`, and :code:`not_in_mouth`
variables are numpy arrays so they need to be combined using the :code:`np.logical_xxx`
functions from numpy.
"""
from stylo.testing.examples import define_benchmarked_example

example_info = {"name": "pacman", "type": "extending"}


def make_pacman():

    # <example>

    import numpy as np

    from stylo.shape import Shape, Circle
    from stylo.color import FillColor
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

    yellow = FillColor("ffff00")
    img = SimpleImage(Pacman(0.75, 1), yellow)

    # </example>

    return img


test_pacman = define_benchmarked_example("pacman", make_pacman)
