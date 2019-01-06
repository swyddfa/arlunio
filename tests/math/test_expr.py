"""This module contains the 'unit tests' for each object in stylo's expression system.

These tests are meant to verify that the individual components function in isolation
as they are expected to.
"""
import pytest
import numpy as np

from unittest import TestCase
from stylo.math.expr import (
    StyAnd,
    StyDivide,
    StyFloorDivide,
    StyGreaterEqual,
    StyGreaterThan,
    StyLessEqual,
    StyLessThan,
    StyMinus,
    StyModulo,
    StyMultiply,
    StyOr,
    StyPlus,
    StyPower,
)
from stylo.testing.math import BaseBinaryOpTest


@pytest.mark.math
class TestStyAnd(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyAnd` binary operation."""

    def setUp(self):
        self.operation = StyAnd
        self.examples = [
            (False, False, False),
            (False, True, False),
            (True, False, False),
            (True, True, True),
            (
                np.array([True, False, True]),
                np.array([False, True, True]),
                np.array([False, False, True]),
            ),
        ]


@pytest.mark.math
class TestStyDivide(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyDivide` binary operation."""

    def setUp(self):
        self.operation = StyDivide
        self.examples = [
            (12, 1, 12),
            (3, 2, 1.5),
            (25, 5, 5),
            (np.array([12, 4, 1]), np.array([4, 2, 1]), np.array([3, 2, 1])),
        ]


@pytest.mark.math
class TestStyFloorDivide(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyFloorDivide` binary operation."""

    def setUp(self):
        self.operation = StyFloorDivide
        self.examples = [
            (12, 1, 12),
            (3, 2, 1),
            (25, 5, 5),
            (np.array([12, 4, 1]), np.array([4, 2, 1]), np.array([3, 2, 1])),
        ]


@pytest.mark.math
class TestStyGreaterEqual(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyGreaterEqual` binary operation."""

    def setUp(self):
        self.operation = StyGreaterEqual
        self.examples = [
            (1, 2, False),
            (2, 2, True),
            (2, 1, True),
            (np.array([1, 2, 3]), np.array([3, 2, 1]), np.array([False, True, True])),
        ]


@pytest.mark.math
class TestStyGreaterThan(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyGreaterThan` binary operation."""

    def setUp(self):
        self.operation = StyGreaterThan
        self.examples = [
            (1, 2, False),
            (2, 2, False),
            (2, 1, True),
            (np.array([1, 2, 3]), np.array([3, 2, 1]), np.array([False, False, True])),
        ]


@pytest.mark.math
class TestStyLessEqual(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyLessEqual` binary operator."""

    def setUp(self):
        self.operation = StyLessEqual
        self.examples = [
            (1, 2, True),
            (2, 2, True),
            (2, 1, False),
            (np.array([1, 2, 3]), np.array([3, 2, 1]), np.array([True, True, False])),
        ]


@pytest.mark.math
class TestStyLessThan(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyLessThan` binary operator."""

    def setUp(self):
        self.operation = StyLessThan
        self.examples = [
            (1, 2, True),
            (2, 2, False),
            (2, 1, False),
            (np.array([1, 2, 3]), np.array([3, 2, 1]), np.array([True, False, False])),
        ]


@pytest.mark.math
class TestStyMinus(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyMinus` binary operation."""

    def setUp(self):
        self.operation = StyMinus
        self.examples = [
            (1, 0, 1),
            (0, 1, -1),
            (12, 6, 6),
            (np.array([3, 2, 1]), np.array([1, 2, 3]), np.array([2, 0, -2])),
        ]


@pytest.mark.math
class TestStyModulo(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyModulo` binary operation."""

    def setUp(self):
        self.operation = StyModulo
        self.examples = [
            (12, 1, 0),
            (12, 5, 2),
            (12, 24, 12),
            (np.array([3, 2, 1]), np.array([1, 2, 3]), np.array([0, 0, 1])),
        ]


@pytest.mark.math
class TestStyMultiply(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyMultiply` binary operation."""

    def setUp(self):
        self.operation = StyMultiply
        self.examples = [
            (2, 1, 2),
            (12, 0, 0),
            (6, 6, 36),
            (np.array([1, 2, 4]), np.array([4, 2, 1]), np.array([4, 4, 4])),
        ]


@pytest.mark.math
class TestStyOr(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyOr` binary operation."""

    def setUp(self):
        self.operation = StyOr
        self.examples = [
            (False, False, False),
            (False, True, True),
            (True, False, True),
            (True, True, True),
            (
                np.array([True, False, True]),
                np.array([False, True, True]),
                np.array([True, True, True]),
            ),
        ]


@pytest.mark.math
class TestStyPlus(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyPlus` binary operation."""

    def setUp(self):
        self.operation = StyPlus
        self.examples = [
            (0, 1, 1),
            (2, 3, 5),
            (1, -1, 0),
            (np.array([1, 2, 3]), np.array([3, 2, 1]), np.array([4, 4, 4])),
        ]


@pytest.mark.math
class TestStyPower(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`StyPower` binary operation."""

    def setUp(self):
        self.operation = StyPower
        self.examples = [
            (1, 2, 1),
            (2, 3, 8),
            (16, 0.5, 4),
            (np.array([1, 2, 3]), np.array([1, 2, 3]), np.array([1, 4, 27])),
        ]
