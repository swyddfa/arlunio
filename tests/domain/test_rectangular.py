from unittest import TestCase

import pytest
import numpy as np
import numpy.testing as npt
from hypothesis import given, assume, example

from stylo.domain.rectangular import RectangularDomain, get_real_domain
from stylo.testing.strategies import real, dimension
from stylo.testing.domain import BaseRealDomainTest


@pytest.mark.domain
class TestRectangularDomain(TestCase, BaseRealDomainTest):
    """Tests for the RectangularDomain class"""

    def setUp(self):
        self.domain = RectangularDomain(-1, 1, -1, 1)

    @given(xmin=real, xmax=real)
    def test_init_checks_x_min_max(self, xmin, xmax):
        """Ensure that the __init__ method checks to see that the value
        of :code:`xmin < xmax`."""

        assume(xmax <= xmin)

        with pytest.raises(ValueError) as err:
            RectangularDomain(xmin, xmax, 0, 1)

        self.assertIn("must be strictly less than", str(err.value))
        self.assertIn("xmin", str(err.value))
        self.assertIn("xmax", str(err.value))

    @given(ymin=real, ymax=real)
    def test_init_checks_y_min_max(self, ymin, ymax):
        """Ensure that the __init__ method checks to see that the value
        of :code:`ymin < ymax`."""

        assume(ymax <= ymin)

        with pytest.raises(ValueError) as err:
            RectangularDomain(0, 1, ymin, ymax)

        self.assertIn("must be strictly less than", str(err.value))
        self.assertIn("ymin", str(err.value))
        self.assertIn("ymax", str(err.value))

    @given(xmin=real)
    def test_xmin_property(self, xmin):
        """Ensure that the :code:`xmin` property works as expected.

        The :code:`xmin` property should:

        - Return the value of :code:`xmin`
        - Be used to set a new value of :code:`xmin`
        """

        domain = RectangularDomain(xmin, xmin + 1, 0, 1)
        self.assertEqual(xmin, domain.xmin)

        domain.xmin = xmin - 2
        self.assertEqual(xmin - 2, domain.xmin)

    def test_xmin_property_checks_value(self):
        """Ensure that the :code:`xmin` property checks the value it is
        given to make sure it makes sense.

        The new value should:

        - Be a numeric value
        - Be strictly less than the current value of :code:`xmax`
        """

        domain = RectangularDomain(0, 1, 0, 1)

        with pytest.raises(TypeError) as err:
            domain.xmin = "String"

        self.assertIn("must be a number", str(err.value))

        with pytest.raises(ValueError) as err:
            domain.xmin = 10

        self.assertIn("must be strictly less than", str(err.value))

    @given(xmax=real)
    def test_xmax_property(self, xmax):
        """Ensure that the :code:`xmax` property works as expected.

        The :code:`xmax` property should:

        - Return the value of :code:`xmax`
        - Be used to set a new value of :code:`xmax`
        """

        domain = RectangularDomain(xmax - 1, xmax, 0, 1)
        self.assertEqual(xmax, domain.xmax)

        domain.xmax = xmax + 2
        self.assertEqual(xmax + 2, domain.xmax)

    def test_xmax_property_checks_value(self):
        """Ensure that the :code:`xmax` property checks the value it is
        given to make sure it makes sense.

        The new value should:

        - Be a numeric value
        - Be strictly greater than the current value of :code:`xmin`
        """

        domain = RectangularDomain(0, 1, 0, 1)

        with pytest.raises(TypeError) as err:
            domain.xmax = "String"

        self.assertIn("must be a number", str(err.value))

        with pytest.raises(ValueError) as err:
            domain.xmax = -1

        self.assertIn("must be strictly larger than", str(err.value))

    @given(ymin=real)
    def test_ymin_property(self, ymin):
        """Ensure that the :code:`ymin` property as expected.

        The :code:`ymin` property should:

        - Return the value of :code:`ymin`
        - Be used to set a new value of :code:`ymin`
        """

        domain = RectangularDomain(0, 1, ymin, ymin + 1)
        self.assertEqual(ymin, domain.ymin)

        domain.ymin = ymin - 2
        self.assertEqual(ymin - 2, domain.ymin)

    def test_ymin_property_checks_value(self):
        """Ensure that the :code:`ymin` property checks the value
        it is given to make sure it makes sense.

        The new value should:

        - Be a numeric value
        - Be strictly less than the value of :code:`ymax`
        """

        domain = RectangularDomain(0, 1, 0, 1)

        with pytest.raises(TypeError) as err:
            domain.ymin = "String"

        self.assertIn("must be a number", str(err.value))

        with pytest.raises(ValueError) as err:
            domain.ymin = 10

        self.assertIn("must be strictly less than", str(err.value))

    @given(ymax=real)
    def test_ymax_property(self, ymax):
        """Ensure that the :code:`ymax` property works as expected.

        The :code:`ymax` property should

        - Return the current value of :code:`ymax`
        - Be used to set a new value of :code:`ymax`
        """

        domain = RectangularDomain(0, 1, ymax - 1, ymax)
        self.assertEqual(ymax, domain.ymax)

        domain.ymax = ymax + 1
        self.assertEqual(ymax + 1, domain.ymax)

    def test_ymax_property_checks_value(self):
        """Ensure that the :code:`ymax` property checks the value it is given
        to make sure it makes sense

        The new value should:

        - Be a numeric value
        - Be strictly greater than :code:`ymin`
        """

        domain = RectangularDomain(0, 1, 0, 1)

        with pytest.raises(TypeError) as err:
            domain.ymax = "String"

        self.assertIn("must be a number", str(err.value))

        with pytest.raises(ValueError) as err:
            domain.ymax = -1

        self.assertIn("must be strictly larger than", str(err.value))

    @given(xmin=real, xmax=real, width=dimension, height=dimension)
    def test_x_property_values(self, width, height, xmin, xmax):
        """Ensure that the :code:`x` property produces the expected values.

        The produced values should

        - Start with xmin
        - End with xmax
        - Be larger than xmin inbetween
        - Be less than xmax inbetween

        .. note::

           We don't have to check the shape of the produced array as that is
           handled by the base class.
        """
        assume(xmin < xmax)
        domain = RectangularDomain(xmin, xmax, 0, 1)

        XS = domain.x(width, height)

        npt.assert_array_equal(XS[:0], xmin)
        npt.assert_array_equal(XS[:, -1], xmax)

        interior = XS[:, 1:-1]
        self.assertTrue(
            (interior <= xmax).all(), "The interior should be less than xmax"
        )
        self.assertTrue(
            (xmin <= interior).all(), "The interior should be greater then xmin"
        )

    @given(ymin=real, ymax=real, width=dimension, height=dimension)
    def test_y_property_values(self, width, height, ymin, ymax):
        """Ensure that the :code:`y` property produces the expected values.

        The produced values should

        - Start with ymax
        - End with ymin
        - Be larger than ymin inbetween
        - Be less than ymax inbetween

        .. note::

           We don't have to check the shape of the produced array as that is
           handled by the base class
        """
        assume(ymin < ymax)
        domain = RectangularDomain(0, 1, ymin, ymax)

        YS = domain.y(width, height)

        npt.assert_array_equal(YS[0, :], ymax)
        npt.assert_array_equal(YS[-1, :], ymin)

        interior = YS[1:-1,]

        self.assertTrue(
            (interior <= ymax).all(), "The interior should be less than ymax"
        )
        self.assertTrue(
            (ymin <= interior).all(), "The interior should be greater than ymin"
        )

    @given(width=dimension, height=dimension)
    def test_r_property_values(self, width, height):
        """Ensure that the :code:`r` property produces the expected values.

        The produced values should

        - All be greater than zero
        - Be radially symmetric but how do we test that??
        """

        domain = RectangularDomain(0, 1, 0, 1)

        RS = domain.r(width, height)
        self.assertTrue((RS >= 0).all(), "Values of r should be strictly positive")

    @given(width=dimension, height=dimension)
    def test_t_property_values(self, width, height):
        """Ensure that :code:`t` property produces the expected values.

        The produced values should

        - Be between -pi and pi
        - Be the same along "radial lines" but how do we test that??
        """

        domain = RectangularDomain(0, 1, 0, 1)

        TS = domain.t(width, height)
        self.assertTrue(
            (TS <= np.pi / 2).all(), "Angles should be less than or equal to pi/2"
        )
        self.assertTrue(
            (TS >= -np.pi / 2).all(), "Angles should be greater than or equal to -pi/2"
        )


@pytest.mark.domain
class TestGetRealDomain:
    """Tests for the :code:`get_real_domain` function."""

    @given(width=dimension)
    @example(width=0)
    def test_checks_width_parameter(self, width):
        """Ensure that an error is thrown if a zero or negative value for :code:`width`
        is given.
        """

        with pytest.raises(ValueError) as err:
            get_real_domain(-width, 4)

        assert "must be a positive number" in str(err.value)

    @given(height=dimension)
    @example(height=0)
    def test_checks_height_parameter(self, height):
        """Ensure that an error is thrown if a zero or negative value for :code:`height`
        is given.
        """

        with pytest.raises(ValueError) as err:
            get_real_domain(4, -height)

        assert "must be a positive number" in str(err.value)

    @given(scale=real)
    @example(scale=0)
    def test_checks_scale_positive(self, scale):
        """Ensure that an error is thrown if a zero or negative value for :code:`scale`
        is given.
        """
        assume(scale >= 0)

        with pytest.raises(ValueError) as err:
            get_real_domain(4, 4, scale=-scale)

        assert "must be strictly positive" in str(err.value)

    @given(width=dimension, height=dimension, scale=real)
    def test_ylength_is_scale(self, width, height, scale):
        """Ensure that the length of the y interval corresponds to the value of the
        scale parameter.
        """
        assume(scale > 0)
        domain = get_real_domain(width, height, scale)

        ymax = domain.ymax
        ymin = domain.ymin

        assert (ymax - ymin) == scale

    @given(width=dimension, height=dimension, scale=real)
    def test_domain_matches_aspect_ratio(self, width, height, scale):
        """Ensure that the aspect ratio of the domain matches the aspect ratio specified
        by the width and height
        """

        assume(scale > 0)
        domain = get_real_domain(width, height, scale)

        ylength = domain.ymax - domain.ymin
        xlength = domain.xmax - domain.xmin

        domain_ratio = xlength / ylength
        aspect_ratio = width / height

        assert domain_ratio == pytest.approx(aspect_ratio, 0.1)
