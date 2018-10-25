import pytest
import numpy as np
from unittest import TestCase
from hypothesis import given, assume


from stylo.domain import SquareDomain
from stylo.shape import Ellipse, Circle, Rectangle, Square, Triangle, Line
from stylo.testing.shape import BaseShapeTest
from stylo.testing.strategies import real


@pytest.mark.shape
class TestEllipse(TestCase, BaseShapeTest):
    """Tests for the :code:`Ellipse` shape."""

    def setUp(self):
        self.shape = Ellipse()

    def test_init_defaults(self):
        """Ensure that :code:`Ellipse` is initialised with sane arguments by
        default."""

        ellipse = Ellipse()

        assert ellipse.x == 0
        assert ellipse.y == 0
        assert ellipse.a == 2
        assert ellipse.b == 1
        assert ellipse.r == 0.5
        assert ellipse.pt == 0.01

        assert not ellipse.fill

    def test_draw_pt(self):
        """Ensure that we can draw a complete ellipse as a curve."""

        ellipse = Ellipse(pt=0.1)
        domain = SquareDomain(-1, 1)

        # fmt: off
        expected = np.array(
            [
                [False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False],
                [False,  True,  True,  True,  True,  True,  True, False],
                [ True, False, False, False, False, False, False,  True],
                [ True, False, False, False, False, False, False,  True],
                [False,  True,  True,  True,  True,  True,  True, False],
                [False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False],
            ]
        )
        # fmt: on

        assert (ellipse(domain, 8, 8) == expected).all()

    def test_draw_fill(self):
        """Ensure that we a draw a complete ellipse as a shaded region."""

        ellipse = Ellipse(fill=True)
        domain = SquareDomain(-1, 1)

        # fmt: off
        expected = np.array(
            [
                [False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False],
                [False, False,  True,  True,  True,  True, False, False],
                [False,  True,  True,  True,  True,  True,  True, False],
                [False,  True,  True,  True,  True,  True,  True, False],
                [False, False,  True,  True,  True,  True, False, False],
                [False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False],
            ]
        )
        # fmt: on

        assert (ellipse(domain, 8, 8) == expected).all()


@pytest.mark.shape
class TestCircle(TestCase, BaseShapeTest):
    """Tests for the :code:`Circle` shape."""

    def setUp(self):
        self.shape = Circle()

    def test_init_defaults(self):
        """Ensure that :code:`Circle` is initialised with sane defaults."""

        circle = Circle()

        assert circle.x == 0
        assert circle.y == 0
        assert circle.r == 0.5

        assert circle.pt == 0.01
        assert not circle.fill

    def test_draw_pt(self):
        """Ensure that we can draw a :code:`Circle` as a curve."""

        circle = Circle(r=0.8, pt=0.15)
        domain = SquareDomain(-1, 1)

        # fmt: off
        expected = np.array(
            [
                [False, False, False, False, False, False, False, False],
                [False, False, True,  True,  True,   True, False, False],
                [False,  True, False, False, False, False,  True, False],
                [False,  True, False, False, False, False,  True, False],
                [False,  True, False, False, False, False,  True, False],
                [False,  True, False, False, False, False,  True, False],
                [False, False,  True,  True,  True,  True, False, False],
                [False, False, False, False, False, False, False, False],
            ]
        )
        # fmt: on

        assert (expected == circle(domain, 8, 8)).all()

    def test_draw_full(self):
        """Ensure that we can draw a :code:`Circle` as a shaded region."""

        circle = Circle(r=0.8, fill=True)
        domain = SquareDomain(-1, 1)

        # fmt: off
        expected = np.array(
            [
                [False, False, False, False, False, False, False, False],
                [False, False, False,  True,  True, False, False, False],
                [False, False,  True,  True,  True,  True, False, False],
                [False,  True,  True,  True,  True,  True,  True, False],
                [False,  True,  True,  True,  True,  True,  True, False],
                [False, False,  True,  True,  True,  True, False, False],
                [False, False, False,  True,  True, False, False, False],
                [False, False, False, False, False, False, False, False],
            ]
        )
        # fmt: on

        assert (expected == circle(domain, 8, 8)).all()


@pytest.mark.shape
class TestRectangle(TestCase, BaseShapeTest):
    """Tests for the :code:`Rectangle` shape."""

    def setUp(self):
        self.shape = Rectangle(0, 0, 0.6, 0.3)


@pytest.mark.shape
class TestSquare(TestCase, BaseShapeTest):
    """Tests for the :code:`Square` shape."""

    def setUp(self):
        self.shape = Square(0, 0, 0.75)


@pytest.mark.shape
class TestTriangle(TestCase, BaseShapeTest):
    """Tests for the :code:`Triangle` shape."""

    def setUp(self):
        self.shape = Triangle((1, 0.5), (0.2, 1), (0.4, 0.5))


@pytest.mark.shape
class TestLine(TestCase, BaseShapeTest):
    """Tests for the :code:`Line` shape."""

    def setUp(self):
        self.shape = Line()

    def test_init_defaults(self):
        """Ensure that the :code:`Line` is created with sane defaults."""

        line = Line()

        assert line.p1 == (0, 0)
        assert line.p2 == (1, 1)
        assert line.pt == 0.01
        assert not line.extend

    @given(x1=real, y1=real, x2=real, y2=real)
    def test_init_sorts_points(self, x1, y1, x2, y2):
        """Ensure that the :code:`Line` object sorts the points by the x coordinate."""

        assume(x1 != x2)

        line = Line((x1, y1), (x2, y2))
        assert line.p1[0] < line.p2[0]

    def test_draw_segment_pt(self):
        """Ensure we can draw a line segment."""

        line = Line(pt=0.1)
        domain = SquareDomain(-1, 1)

        # fmt: off
        expected = np.array(
            [
                [False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False,  True, False],
                [False, False, False, False, False,  True, False, False],
                [False, False, False, False,  True, False, False, False],
                [False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False],
            ]
        )
        # fmt: on

        assert (expected == line(domain, 8, 8)).all()

    def test_draw_line_pt(self):
        """Ensure that we can draw a line that's been extended to infinity."""

        line = Line(pt=0.1, extend=True)
        domain = SquareDomain(-1, 1)

        # fmt: off
        expected = np.array(
            [
                [False, False, False, False, False, False, False,  True],
                [False, False, False, False, False, False,  True, False],
                [False, False, False, False, False,  True, False, False],
                [False, False, False, False,  True, False, False, False],
                [False, False, False,  True, False, False, False, False],
                [False, False,  True, False, False, False, False, False],
                [False,  True, False, False, False, False, False, False],
                [ True, False, False, False, False, False, False, False],
            ]
        )
        # fmt: on

        assert (expected == line(domain, 8, 8)).all()

    def test_draw_line_below(self):
        """Ensure that we can draw a shaded region underneath a line."""

        line = Line(pt=0.1, extend=True, below=True)
        domain = SquareDomain(-1, 1)

        # fmt: off
        expected = np.array(
            [
                [False, False, False, False, False, False, False,  True],
                [False, False, False, False, False, False, False,  True],
                [False, False, False, False, False, False,  True,  True],
                [False, False, False, False, False,  True,  True,  True],
                [False, False, False, False,  True,  True,  True,  True],
                [False, False, False,  True,  True,  True,  True,  True],
                [False, False,  True,  True,  True,  True,  True,  True],
                [ True,  True,  True,  True,  True,  True,  True,  True],
            ]
        )
        # fmt: on
        assert (expected == line(domain, 8, 8)).all()

    def test_draw_line_above(self):
        """Ensure that we can draw a shaded region above a line."""

        line = Line(pt=0.1, extend=True, above=True)
        domain = SquareDomain(-1, 1)

        # fmt: off
        expected = np.array(
            [
                [True,  True,  True,  True,  True,  True,  True,  True],
                [True,  True,  True,  True,  True,  True,  True, False],
                [True,  True,  True,  True,  True,  True, False, False],
                [True,  True,  True,  True,  True, False, False, False],
                [True,  True,  True,  True, False, False, False, False],
                [True,  True,  True, False, False, False, False, False],
                [True,  True, False, False, False, False, False, False],
                [True, False, False, False, False, False, False, False],
            ]
        )
        # fmt: on
        assert (expected == line(domain, 8, 8)).all()
