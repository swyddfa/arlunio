import numpy as np

from math import sqrt, pi
from pytest import raises
from hypothesis import given, assume
from hypothesis.strategies import floats, tuples, integers, one_of,\
                                  composite

from stylo.drawable import Domain


# Some useful strategies
real = floats(min_value=-1e6, max_value=1e6)
domain = tuples(real, real).filter(lambda x: x[0] < x[1])
size = integers(min_value=2, max_value=512)


class TestInit(object):

    def test_default_init(self):

        d = Domain()

        assert d._xmin == -1
        assert d._ymin == -1
        assert d._xmax == 1
        assert d._ymax == 1

        # There should also have been a dictionary defined which
        # contains the 'instructions' for constructing coordinate
        # grids
        assert isinstance(d._coords, (dict))
        assert 'x' in d._coords.keys()
        assert 'y' in d._coords.keys()
        assert 'r' in d._coords.keys()
        assert 't' in d._coords.keys()

        for item in d._coords.values():
            assert callable(item)
            assert item.__code__.co_argcount == 2


    @given(xmin=real, xmax=real, ymin=real, ymax=real)
    def test_init_with_values(self, xmin, xmax, ymin, ymax):

        assume(xmin < xmax)
        assume(ymin < ymax)

        d = Domain(xmin, xmax, ymin, ymax)

        assert d._xmin == xmin
        assert d._ymin == ymin
        assert d._xmax == xmax
        assert d._ymax == ymax

        # There should also have been a dictionary defined which
        # contains the 'instructions' for constructing coordinate
        # grids
        assert isinstance(d._coords, (dict))
        assert 'x' in d._coords.keys()
        assert 'y' in d._coords.keys()
        assert 'r' in d._coords.keys()
        assert 't' in d._coords.keys()

        for item in d._coords.values():
            assert callable(item)
            assert item.__code__.co_argcount == 2

    @given(xmin=real, xmax=real, ymin=real, ymax=real)
    def test_init_with_bad_xvalues(self, xmin, xmax, ymin, ymax):

        assume(xmin >= xmax)
        assume(ymin < ymax)

        with raises(ValueError) as err:
            d = Domain(xmin, xmax, ymin, ymax)

        assert 'x_min must be less than x_max' in str(err.value)

    @given(xmin=real, xmax=real, ymin=real, ymax=real)
    def test_init_with_bad_xvalues(self, xmin, xmax, ymin, ymax):

        assume(ymin >= ymax)
        assume(xmin < xmax)

        with raises(ValueError) as err:
            d = Domain(xmin, xmax, ymin, ymax)

        assert 'y_min must be less than y_max' in str(err.value)


class TestProperties(object):

    @given(xs=domain, ys=domain)
    def test_str_property(self, xs, ys):

        d = Domain(xs[0], xs[1], ys[0], ys[1])

        s = str(d)

        assert s == '[{}, {}] x [{}, {}]'.format(*xs, *ys)


    @given(xs=domain, ys=domain, width=size, height=size)
    def test_X_property(self, xs, ys, width, height):

        d = Domain(*xs, *ys)
        mk_xs = d._X

        assert callable(mk_xs)
        assert mk_xs.__code__.co_argcount == 2

        coords = mk_xs(width, height)

        # The generated grid should be height x width
        assert coords.shape == (height, width)

        # Each row should be the same
        coords = np.unique(coords, axis=0)
        assert coords.shape == (1, width)
        coords.shape = (width,)

        # The max should be the upper x value
        # and the last
        assert np.max(coords) == xs[1]
        assert coords[-1] == xs[1]

        # The min should be the lowest x value
        # and the first
        assert np.min(coords) == xs[0]
        assert coords[0] == xs[0]


    @given(xs=domain, ys=domain, width=size, height=size)
    def test_Y_property(self, xs, ys, width, height):

        d = Domain(*xs, *ys)
        mk_ys = d._Y

        # The result should be a function in width and height
        assert callable(mk_ys)
        assert mk_ys.__code__.co_argcount == 2

        coords = mk_ys(width, height)

        # Again the grid should be height x width
        assert coords.shape == (height, width)

        # Each column should be the same
        coords = np.unique(coords, axis=1)
        assert coords.shape == (height, 1)
        coords.shape = (height,)

        # The max should be the upper y value
        # and the first
        assert np.max(coords) == ys[1]
        assert coords[0] == ys[-1]

        # The min should be the lower y value
        # and the last
        assert np.min(coords) == ys[0]
        assert coords[-1] == ys[0]


    @given(xs=domain, ys=domain, width=size, height=size)
    def test_R_property(self, xs, ys, width, height):

        d = Domain(*xs, *ys)
        mk_rs = d._R

        # The result should be a function in width and height
        assert callable(mk_rs)
        assert mk_rs.__code__.co_argcount == 2

        coords = mk_rs(width, height)

        # Again the grid should be height x width
        assert coords.shape == (height, width)

        # I would like a nice way to select 'circles'
        # in the generated grid and assert that they
        # are equal.
        assert np.min(coords) >= 0.0

    @given(xs=domain, ys=domain, width=size, height=size)
    def test_T_property(self, xs, ys, width, height):

        d = Domain(*xs, *ys)
        mk_ts = d._T

        # The result should be a function in width and height
        assert callable(mk_ts)
        assert mk_ts.__code__.co_argcount == 2

        coords = mk_ts(width, height)

        # Again the grid should be height x width
        assert coords.shape == (height, width)

        assert np.min(coords) >= -pi
        assert np.max(coords) <= pi


class TestGetItem(object):
    pass
