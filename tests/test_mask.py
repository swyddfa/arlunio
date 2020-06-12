import numpy as np
import numpy.random as npr
import py.test

from hypothesis import given
from hypothesis.strategies import integers

import arlunio as ar
import arlunio.testing as T

from arlunio.mask import Mask


@ar.definition
def MaskGenerator(width: int, height: int, *, seed=1024) -> Mask:
    """A generator of random masks."""

    gen = npr.default_rng(seed=seed)
    return Mask(gen.random(size=(height, width)) < 0.5)


class TestMask:
    """Test cases for the :code:`Mask` type."""

    @py.test.mark.parametrize(
        "arr", [np.array([True, False, True]), np.array([[True, False], [False, True]])]
    )
    def test_init(self, arr):
        """Ensure that masks can be created directly from an existing array,"""

        mask = Mask(arr)

        assert isinstance(mask, Mask)
        assert (mask == arr).all()

    @py.test.mark.parametrize(
        "arr", [np.array([True, False, True]), np.array([[True, False], [False, True]])]
    )
    def test_init_view(self, arr):
        """Ensure that masks can be created as a view on an existing numpy array."""

        mask = arr.view(Mask)

        assert isinstance(mask, Mask)
        assert (mask == arr).all()

    @py.test.mark.parametrize(
        "id, a, b, expected",
        [
            (
                "broadcast with 'a = True'",
                True,
                Mask(np.array([True, False, True])),
                Mask(np.full(3, True)),
            ),
            (
                "broadcast with 'a = False'",
                False,
                Mask(np.array([True, False, True])),
                Mask(np.array([True, False, True])),
            ),
            (
                "broadcast with 'b = True'",
                Mask(np.array([True, False, True])),
                True,
                Mask(np.full(3, True)),
            ),
            (
                "broadcast with 'b = False'",
                Mask(np.array([True, False, True])),
                False,
                Mask(np.array([True, False, True])),
            ),
            (
                "broadcast with a = array",
                np.array([True, False]),
                Mask(np.array([[False, True], [True, False]])),
                Mask(np.array([[True, True], [True, False]])),
            ),
            (
                "broadcast with b = array",
                Mask(np.array([[False, True], [True, False]])),
                np.array([True, False]),
                Mask(np.array([[True, True], [True, False]])),
            ),
            (
                "one mask, one array of equal size",
                Mask(np.array([True, False, True])),
                np.array([False, True, False]),
                Mask(np.array([True, True, True])),
            ),
            (
                "one array, one mask of equal size",
                np.array([False, True, False]),
                Mask(np.array([True, False, True])),
                Mask(np.array([True, True, True])),
            ),
            (
                "two masks of equal size",
                Mask(np.array([False, True, False])),
                Mask(np.array([True, False, True])),
                Mask(np.array([True, True, True])),
            ),
        ],
    )
    def test_add(self, id, a, b, expected):
        """Ensure that masks can be added together, where 'add' in this case is a
        boolean OR"""

        result = a + b

        assert isinstance(result, Mask), "The result should also be a mask"
        assert (result == expected).all()

    @py.test.mark.parametrize(
        "id, a, b, expected",
        [
            (
                "broadcast with 'a = True",
                True,
                Mask(np.array([True, False, True])),
                Mask(np.array([True, False, True])),
            ),
            (
                "broadcast with 'a = False",
                False,
                Mask(np.array([True, False, True])),
                Mask(np.full(3, False)),
            ),
            (
                "broadcast with 'b = True'",
                Mask(np.array([True, False, True])),
                True,
                Mask(np.array([True, False, True])),
            ),
            (
                "broadcast with 'b = False'",
                Mask(np.array([True, False, True])),
                False,
                Mask(np.array([False, False, False])),
            ),
            (
                "broadcast with a = array",
                np.array([True, False]),
                Mask(np.array([[True, False], [False, True]])),
                Mask(np.array([[True, False], [False, False]])),
            ),
            (
                "broadcast with b = array",
                Mask(np.array([[True, False], [False, True]])),
                np.array([True, False]),
                Mask(np.array([[True, False], [False, False]])),
            ),
            (
                "one mask, one array of equal size",
                Mask(np.array([True, False, True])),
                np.array([True, True, False]),
                Mask(np.array([True, False, False])),
            ),
            (
                "one array, one mask of equal size",
                np.array([True, True, False]),
                Mask(np.array([True, False, True])),
                Mask(np.array([True, False, False])),
            ),
            (
                "two masks of equal size",
                Mask(np.array([True, False, True])),
                Mask(np.array([True, True, False])),
                Mask(np.array([True, False, False])),
            ),
        ],
    )
    def test_mul(self, id, a, b, expected):
        """Ensure that masks can be multiplied together, where 'mul' in this case is a
        boolean AND."""

        result = a * b

        assert isinstance(result, Mask), "The result should also be a mask"
        assert (result == expected).all()

    @py.test.mark.parametrize(
        "id, a, b, expected",
        [
            (
                "1D base, 1D sub-selection",
                Mask(np.array([True, False, True, False, True])),
                np.array([True, False, True]),
                Mask(np.array([True, False, False, False, True])),
            ),
            (
                "2D base, 1D sub-selection",
                Mask(np.array([[True, True], [True, False]])),
                np.array([True, False, False]),
                Mask(np.array([[True, False], [False, False]])),
            ),
            (
                "2D base, 2D sub-selection",
                Mask(np.full((3, 3), (True, False, True))),
                np.array([[True, False], [True, False], [False, True]]),
                Mask(
                    np.array(
                        [
                            [True, False, False],
                            [True, False, False],
                            [False, False, True],
                        ]
                    )
                ),
            ),
        ],
    )
    def test_mul_selection(self, id, a, b, expected):
        """Ensure that when arrays don't broadcast but the shape matches with a
        selection, the second array is combined with it to create a sub-selection."""

        result = a * b

        assert isinstance(result, Mask), "The result should also be a mask"
        assert (result == expected).all()

    @py.test.mark.parametrize(
        "id, a, b, expected",
        [
            (
                "broadcast with 'b = True'",
                Mask(np.array([True, False, True])),
                True,
                Mask(np.full(3, False)),
            ),
            (
                "broadcast with 'b = False'",
                Mask(np.array([True, False, True])),
                False,
                Mask(np.array([True, False, True])),
            ),
            (
                "broadcast with b = array",
                Mask(np.array([[True, False], [False, True]])),
                np.array([True, False]),
                Mask(np.array([[False, False], [False, True]])),
            ),
            (
                "one mask, one array of equal size",
                Mask(np.array([True, False, True])),
                np.array([True, True, False]),
                Mask(np.array([False, False, True])),
            ),
            (
                "one array, one mask of equal size",
                np.array([True, True, False]),
                Mask(np.array([True, False, True])),
                Mask(np.array([False, True, False])),
            ),
            (
                "two masks of equal size",
                Mask(np.array([True, False, True])),
                Mask(np.array([True, True, False])),
                Mask(np.array([False, False, True])),
            ),
        ],
    )
    def test_sub(self, id, a, b, expected):
        """Ensure that masks can be subtracted, where 'subtract' is the same as
        'a AND (NOT b)'."""

        result = a - b

        assert isinstance(result, Mask), "The result should also be a mask"
        assert (result == expected).all()

    @py.test.mark.parametrize(
        "id, shape, expected",
        [
            ("no arguments", None, Mask(False)),
            ("shape as tuple", ((3, 2),), Mask(np.full((3, 2), False))),
            ("shape as ints", (3, 2), Mask(np.full((3, 2), False))),
        ],
    )
    def test_empty(self, id, shape, expected):
        """Ensure that we can generate an empty mask with the given shape."""

        mask = Mask.empty() if shape is None else Mask.empty(*shape)

        assert isinstance(mask, Mask)
        assert (mask == expected).all()

    @py.test.mark.parametrize(
        "id, shape, expected",
        [
            ("no arguments", None, Mask(True)),
            ("shape as tuple", ((3, 2),), Mask(np.full((3, 2), True))),
            ("shape as ints", (3, 2), Mask(np.full((3, 2), True))),
        ],
    )
    def test_full(self, id, shape, expected):
        """Ensure that we can generate an empty mask with the given shape."""

        mask = Mask.full() if shape is None else Mask.full(*shape)

        assert isinstance(mask, Mask)
        assert (mask == expected).all()


class TestOperators:
    """Test cases for the operators defined for mask definitions."""

    @given(width=T.dimension, height=T.dimension, seed=integers(min_value=1))
    def test_add_operator(self, width, height, seed):
        """Ensure that when adding, combining definitions then calling is the
        same as calling the definitions then combining."""

        a = MaskGenerator(seed=seed)
        b = MaskGenerator(seed=seed + 1)

        r1 = (a + b)(width=width, height=height)

        a = MaskGenerator(seed=seed)
        b = MaskGenerator(seed=seed + 1)

        r2 = a(width=width, height=height) + b(width=width, height=height)

        assert (r1 == r2).all()

    @given(width=T.dimension, height=T.dimension, seed=integers(min_value=1))
    def test_mul_operator(self, width, height, seed):
        """Ensure that when multiplying, combining definitions then calling is the same
        as calling the definitions then combining."""

        a = MaskGenerator(seed=seed)
        b = MaskGenerator(seed=seed + 1)

        r1 = (a * b)(width=width, height=height)

        a = MaskGenerator(seed=seed)
        b = MaskGenerator(seed=seed + 1)

        r2 = a(width=width, height=height) * b(width=width, height=height)

        assert (r1 == r2).all()

    @given(width=T.dimension, height=T.dimension, seed=integers(min_value=1))
    def test_sub_operator(self, width, height, seed):
        """Ensure that when subtracting, combining definitions then calling is the same
        as calling the definitions then combining."""

        a = MaskGenerator(seed=seed)
        b = MaskGenerator(seed=seed + 1)

        r1 = (a - b)(width=width, height=height)

        a = MaskGenerator(seed=seed)
        b = MaskGenerator(seed=seed + 1)

        r2 = a(width=width, height=height) - b(width=width, height=height)

        assert (r1 == r2).all()
