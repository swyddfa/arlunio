"""This module contains the 'unit tests' for each object in stylo's expression system.

These tests are meant to verify that the individual components function in isolation
as they are expected to.
"""
import pytest
import numpy as np

from unittest import TestCase
from stylo.math.expr import (
    And,
    Divide,
    FloorDivide,
    GreaterEqual,
    GreaterThan,
    LessEqual,
    LessThan,
    Minus,
    Modulo,
    Multiply,
    Or,
    Plus,
    Power,
)
from stylo.testing.math import BaseBinaryOpTest


@pytest.mark.math
class TestAnd(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`And` binary operation."""

    def setUp(self):
        self.operation = And
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
class TestDivide(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`Divide` binary operation."""

    def setUp(self):
        self.operation = Divide
        self.examples = [
            (12, 1, 12),
            (3, 2, 1.5),
            (25, 5, 5),
            (np.array([12, 4, 1]), np.array([4, 2, 1]), np.array([3, 2, 1])),
        ]


@pytest.mark.math
class TestFloorDivide(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`FloorDivide` binary operation."""

    def setUp(self):
        self.operation = FloorDivide
        self.examples = [
            (12, 1, 12),
            (3, 2, 1),
            (25, 5, 5),
            (np.array([12, 4, 1]), np.array([4, 2, 1]), np.array([3, 2, 1])),
        ]


@pytest.mark.math
class TestGreaterEqual(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`GreaterEqual` binary operation."""

    def setUp(self):
        self.operation = GreaterEqual
        self.examples = [
            (1, 2, False),
            (2, 2, True),
            (2, 1, True),
            (np.array([1, 2, 3]), np.array([3, 2, 1]), np.array([False, True, True])),
        ]


@pytest.mark.math
class TestGreaterThan(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`GreaterThan` binary operation."""

    def setUp(self):
        self.operation = GreaterThan
        self.examples = [
            (1, 2, False),
            (2, 2, False),
            (2, 1, True),
            (np.array([1, 2, 3]), np.array([3, 2, 1]), np.array([False, False, True])),
        ]


@pytest.mark.math
class TestLessEqual(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`LessEqual` binary operator."""

    def setUp(self):
        self.operation = LessEqual
        self.examples = [
            (1, 2, True),
            (2, 2, True),
            (2, 1, False),
            (np.array([1, 2, 3]), np.array([3, 2, 1]), np.array([True, True, False])),
        ]


@pytest.mark.math
class TestLessThan(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`LessThan` binary operator."""

    def setUp(self):
        self.operation = LessThan
        self.examples = [
            (1, 2, True),
            (2, 2, False),
            (2, 1, False),
            (np.array([1, 2, 3]), np.array([3, 2, 1]), np.array([True, False, False])),
        ]


@pytest.mark.math
class TestMinus(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`Minus` binary operation."""

    def setUp(self):
        self.operation = Minus
        self.examples = [
            (1, 0, 1),
            (0, 1, -1),
            (12, 6, 6),
            (np.array([3, 2, 1]), np.array([1, 2, 3]), np.array([2, 0, -2])),
        ]


@pytest.mark.math
class TestModulo(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`Modulo` binary operation."""

    def setUp(self):
        self.operation = Modulo
        self.examples = [
            (12, 1, 0),
            (12, 5, 2),
            (12, 24, 12),
            (np.array([3, 2, 1]), np.array([1, 2, 3]), np.array([0, 0, 1])),
        ]


@pytest.mark.math
class TestMultiply(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`Multiply` binary operation."""

    def setUp(self):
        self.operation = Multiply
        self.examples = [
            (2, 1, 2),
            (12, 0, 0),
            (6, 6, 36),
            (np.array([1, 2, 4]), np.array([4, 2, 1]), np.array([4, 4, 4])),
        ]


@pytest.mark.math
class TestOr(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`Or` binary operation."""

    def setUp(self):
        self.operation = Or
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
class TestPlus(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`Plus` binary operation."""

    def setUp(self):
        self.operation = Plus
        self.examples = [
            (0, 1, 1),
            (2, 3, 5),
            (1, -1, 0),
            (np.array([1, 2, 3]), np.array([3, 2, 1]), np.array([4, 4, 4])),
        ]


@pytest.mark.math
class TestPower(TestCase, BaseBinaryOpTest):
    """Tests for the :code:`Power` binary operation."""

    def setUp(self):
        self.operation = Power
        self.examples = [
            (1, 2, 1),
            (2, 3, 8),
            (16, 0.5, 4),
            (np.array([1, 2, 3]), np.array([1, 2, 3]), np.array([1, 4, 27])),
        ]
