import numpy as np
import numpy.random as npr
import py.test
from hypothesis import given
from hypothesis.strategies import integers

import arlunio as ar
import arlunio.mask as mask
import arlunio.testing as T


@ar.definition
def MaskGenerator(width: int, height: int, *, seed=1024) -> mask.Mask:
    """A generator of random masks."""

    gen = npr.default_rng(seed=seed)
    return mask.Mask(gen.random(size=(height, width)) < 0.5)


class TestMask:
    """Test cases for the :code:`Mask` type."""

    @py.test.mark.parametrize(
        "arr", [np.array([True, False, True]), np.array([[True, False], [False, True]])]
    )
    def test_init(self, arr):
        """Ensure that masks can be created directly from an existing array,"""

        m = mask.Mask(arr)

        assert isinstance(m, mask.Mask)
        assert (m == arr).all()

    @py.test.mark.parametrize(
        "arr", [np.array([True, False, True]), np.array([[True, False], [False, True]])]
    )
    def test_init_view(self, arr):
        """Ensure that masks can be created as a view on an existing numpy array."""

        m = arr.view(mask.Mask)

        assert isinstance(m, mask.Mask)
        assert (m == arr).all()

    @py.test.mark.parametrize(
        "id, a, b, expected",
        [
            (
                "broadcast with 'a = True'",
                True,
                mask.Mask(np.array([True, False, True])),
                mask.Mask(np.full(3, True)),
            ),
            (
                "broadcast with 'a = False'",
                False,
                mask.Mask(np.array([True, False, True])),
                mask.Mask(np.array([True, False, True])),
            ),
            (
                "broadcast with 'b = True'",
                mask.Mask(np.array([True, False, True])),
                True,
                mask.Mask(np.full(3, True)),
            ),
            (
                "broadcast with 'b = False'",
                mask.Mask(np.array([True, False, True])),
                False,
                mask.Mask(np.array([True, False, True])),
            ),
            (
                "broadcast with a = array",
                np.array([True, False]),
                mask.Mask(np.array([[False, True], [True, False]])),
                mask.Mask(np.array([[True, True], [True, False]])),
            ),
            (
                "broadcast with b = array",
                mask.Mask(np.array([[False, True], [True, False]])),
                np.array([True, False]),
                mask.Mask(np.array([[True, True], [True, False]])),
            ),
            (
                "one mask, one array of equal size",
                mask.Mask(np.array([True, False, True])),
                np.array([False, True, False]),
                mask.Mask(np.array([True, True, True])),
            ),
            (
                "one array, one mask of equal size",
                np.array([False, True, False]),
                mask.Mask(np.array([True, False, True])),
                mask.Mask(np.array([True, True, True])),
            ),
            (
                "two masks of equal size",
                mask.Mask(np.array([False, True, False])),
                mask.Mask(np.array([True, False, True])),
                mask.Mask(np.array([True, True, True])),
            ),
        ],
    )
    def test_add(self, id, a, b, expected):
        """Ensure that masks can be added together, where 'add' in this case is a
        boolean OR"""

        result = a + b

        assert isinstance(result, mask.Mask), "The result should also be a mask"
        assert (result == expected).all()

    @py.test.mark.parametrize(
        "id, a, b, expected",
        [
            (
                "broadcast with 'a = True",
                True,
                mask.Mask(np.array([True, False, True])),
                mask.Mask(np.array([True, False, True])),
            ),
            (
                "broadcast with 'a = False",
                False,
                mask.Mask(np.array([True, False, True])),
                mask.Mask(np.full(3, False)),
            ),
            (
                "broadcast with 'b = True'",
                mask.Mask(np.array([True, False, True])),
                True,
                mask.Mask(np.array([True, False, True])),
            ),
            (
                "broadcast with 'b = False'",
                mask.Mask(np.array([True, False, True])),
                False,
                mask.Mask(np.array([False, False, False])),
            ),
            (
                "broadcast with a = array",
                np.array([True, False]),
                mask.Mask(np.array([[True, False], [False, True]])),
                mask.Mask(np.array([[True, False], [False, False]])),
            ),
            (
                "broadcast with b = array",
                mask.Mask(np.array([[True, False], [False, True]])),
                np.array([True, False]),
                mask.Mask(np.array([[True, False], [False, False]])),
            ),
            (
                "one mask, one array of equal size",
                mask.Mask(np.array([True, False, True])),
                np.array([True, True, False]),
                mask.Mask(np.array([True, False, False])),
            ),
            (
                "one array, one mask of equal size",
                np.array([True, True, False]),
                mask.Mask(np.array([True, False, True])),
                mask.Mask(np.array([True, False, False])),
            ),
            (
                "two masks of equal size",
                mask.Mask(np.array([True, False, True])),
                mask.Mask(np.array([True, True, False])),
                mask.Mask(np.array([True, False, False])),
            ),
        ],
    )
    def test_mul(self, id, a, b, expected):
        """Ensure that masks can be multiplied together, where 'mul' in this case is a
        boolean AND."""

        result = a * b

        assert isinstance(result, mask.Mask), "The result should also be a mask"
        assert (result == expected).all()

    @py.test.mark.parametrize(
        "id, a, b, expected",
        [
            (
                "1D base, 1D sub-selection",
                mask.Mask(np.array([True, False, True, False, True])),
                np.array([True, False, True]),
                mask.Mask(np.array([True, False, False, False, True])),
            ),
            (
                "2D base, 1D sub-selection",
                mask.Mask(np.array([[True, True], [True, False]])),
                np.array([True, False, False]),
                mask.Mask(np.array([[True, False], [False, False]])),
            ),
            (
                "2D base, 2D sub-selection",
                mask.Mask(np.full((3, 3), (True, False, True))),
                np.array([[True, False], [True, False], [False, True]]),
                mask.Mask(
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

        assert isinstance(result, mask.Mask), "The result should also be a mask"
        assert (result == expected).all()

    @py.test.mark.parametrize(
        "id, a, b, expected",
        [
            (
                "broadcast with 'b = True'",
                mask.Mask(np.array([True, False, True])),
                True,
                mask.Mask(np.full(3, False)),
            ),
            (
                "broadcast with 'b = False'",
                mask.Mask(np.array([True, False, True])),
                False,
                mask.Mask(np.array([True, False, True])),
            ),
            (
                "broadcast with b = array",
                mask.Mask(np.array([[True, False], [False, True]])),
                np.array([True, False]),
                mask.Mask(np.array([[False, False], [False, True]])),
            ),
            (
                "one mask, one array of equal size",
                mask.Mask(np.array([True, False, True])),
                np.array([True, True, False]),
                mask.Mask(np.array([False, False, True])),
            ),
            (
                "one array, one mask of equal size",
                np.array([True, True, False]),
                mask.Mask(np.array([True, False, True])),
                mask.Mask(np.array([False, True, False])),
            ),
            (
                "two masks of equal size",
                mask.Mask(np.array([True, False, True])),
                mask.Mask(np.array([True, True, False])),
                mask.Mask(np.array([False, False, True])),
            ),
        ],
    )
    def test_sub(self, id, a, b, expected):
        """Ensure that masks can be subtracted, where 'subtract' is the same as
        'a AND (NOT b)'."""

        result = a - b

        assert isinstance(result, mask.Mask), "The result should also be a mask"
        assert (result == expected).all()

    @py.test.mark.parametrize(
        "id, shape, expected",
        [
            ("no arguments", None, mask.Mask(False)),
            ("shape as tuple", ((3, 2),), mask.Mask(np.full((3, 2), False))),
            ("shape as ints", (3, 2), mask.Mask(np.full((3, 2), False))),
        ],
    )
    def test_empty(self, id, shape, expected):
        """Ensure that we can generate an empty mask with the given shape."""

        m = mask.Mask.empty() if shape is None else mask.Mask.empty(*shape)

        assert isinstance(m, mask.Mask)
        assert (m == expected).all()

    @py.test.mark.parametrize(
        "id, shape, expected",
        [
            ("no arguments", None, mask.Mask(True)),
            ("shape as tuple", ((3, 2),), mask.Mask(np.full((3, 2), True))),
            ("shape as ints", (3, 2), mask.Mask(np.full((3, 2), True))),
        ],
    )
    def test_full(self, id, shape, expected):
        """Ensure that we can generate an empty mask with the given shape."""

        m = mask.Mask.full() if shape is None else mask.Mask.full(*shape)

        assert isinstance(m, mask.Mask)
        assert (m == expected).all()


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


class TestPixelize:
    """Tests for the pixelize definition."""

    @py.test.mark.parametrize(
        "args, message", [({}, "provide a mask or a mask producing definition"),],
    )
    def test_validation(self, args, message):
        """Ensure that the definition checks it is being setup correctly."""

        with py.test.raises(ValueError) as err:
            pix = mask.Pixelize(**args)
            pix(width=4, height=4)

        assert message in str(err.value)
