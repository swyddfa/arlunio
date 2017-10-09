import numpy as np

from hypothesis import given, assume
from hypothesis.strategies import floats, integers, composite
from pytest import raises
from unittest import mock

from stylo.interpolate import Sampler

# Some useful strategies
numpoints = integers(min_value=2, max_value=1000)
value = floats(min_value=-1e6, max_value=1e6)


@composite
def linear_transform(draw):
    m = draw(value)
    c = draw(value)

    return lambda x: m*x + c


class TestProperties(object):

    @given(N=numpoints)
    @mock.patch.object(Sampler, '_sample')
    def test_num_points_with_good_values(self, mock_sample, N):

        s = Sampler()

        # The sample function should already have been called
        assert mock_sample.call_count == 1

        # By default num_points should be 25
        assert s.num_points == 25

        # We should be able to change this
        s.num_points = N
        assert s.num_points == N

        # Now the _sample function should have been called again
        assert mock_sample.call_count == 2

    @given(N=integers(max_value=1, min_value=-1e6))
    @mock.patch.object(Sampler, '_sample')
    def test_num_points_with_bad_values(self, mock_sample, N):

        s = Sampler()

        # The usual defaults should have happened
        assert mock_sample.call_count == 1
        assert s.num_points == 25

        with raises(TypeError) as err:
            s.num_points = 'string'

        # We should have the correct error msg and nothing
        # should have changed
        assert 'must be an integer' in str(err.value)
        assert s.num_points == 25
        assert mock_sample.call_count == 1

        with raises(ValueError) as err:
            s.num_points = N

        assert 'be larger than 1' in str(err.value)
        assert s.num_points == 25
        assert mock_sample.call_count == 1

    @given(N=numpoints)
    def test_len_property(self, N):

        s = Sampler(num_points=N)

        # Each of num_points, len() and len(self._data)
        # should give the same value
        testarr = np.array([s.num_points, len(s), len(s._data)])
        assert (testarr == N).all()

    @given(x=value)
    @mock.patch.object(Sampler, '_sample')
    def test_f_property_with_good_values(self, mock_sample, x):

        s = Sampler()

        # The sample function should have already been called
        assert mock_sample.call_count == 1

        # The default function should be the identity
        assert s(x) == x

        # We should be able to change this
        def squared(y):
            return y * y

        s.f = squared

        # The sample function should once again have been called
        assert mock_sample.call_count == 2

        # The new function should have taken effect
        assert s(x) == x * x

    @mock.patch.object(Sampler, '_sample')
    def test_f_property_with_bad_values(self, mock_sample):

        s = Sampler()

        # The sample function should have already been called
        assert mock_sample.call_count == 1

        # The f property should be callable
        with raises(TypeError) as err:
            s.f = 2

        assert 'must be a function' in str(err.value)
        assert mock_sample.call_count == 1

    @given(a=value, b=value)
    @mock.patch.object(Sampler, '_sample')
    def test_domain_property_with_good_values(self, mock_sample, a, b):
        assume(a < b)

        s = Sampler()

        # The sample function should have been called
        assert mock_sample.call_count == 1

        # By default it should be the interval [0, 1]
        assert s.domain == [0, 1]

        # We should be able to change it
        s.domain = [a, b]
        assert s.domain == [a, b]

        # The sample function should have been called again
        assert mock_sample.call_count == 2

    @given(a=value, b=value)
    @mock.patch.object(Sampler, '_sample')
    def test_domain_property_with_bad_values(self, mock_sample, a, b):
        assume(a < b)

        s = Sampler()

        # The sample function should have been called
        assert mock_sample.call_count == 1

        # It should complain if we try and pass the wrong thing
        with raises(TypeError) as err:
            s.domain = 2.3

        assert 'must be a list in the form [a,b]' in str(err.value)
        assert s.domain == [0, 1]
        assert mock_sample.call_count == 1

        with raises(ValueError) as err:
            s.domain = [b, a]

        assert 'strictly less than' in str(err.value)
        assert s.domain == [0, 1]
        assert mock_sample.call_count == 1


class TestOperations(object):

    @given(y=value, f=linear_transform())
    def test_neg(self, y, f):

        a = Sampler(f)
        b = -a

        assert b(y) == -a(y)

    @given(y=value, f=linear_transform(), g=linear_transform())
    def test_add(self, y, f, g):

        a = Sampler(f)
        b = Sampler(g)

        # Addition of Samplers should 'do the right thing'
        c = a + b

        assert c(y) == a(y) + b(y)

    def test_add_throws_errors(self):

        a = Sampler()

        with raises(TypeError) as err:
            a + 3

        assert 'supported between Sampler objects' in str(err.value)

    @given(x=value, f=linear_transform(), g=linear_transform())
    def test_sub(self, x, f, g):

        a = Sampler(f)
        b = Sampler(g)

        # Subtraction should 'do the right thing'
        c = a - b

        assert c(x) == a(x) - b(x)

    def test_sub_throws_error(self):

        a = Sampler()

        with raises(TypeError) as err:
            a - 2

        assert 'supported between Sampler objects' in str(err.value)

    @given(x=value, f=linear_transform(), g=linear_transform())
    def test_mul(self, x, f, g):

        a = Sampler(f)
        b = Sampler(g)

        # Multiplication should 'do the right thing'
        c = a * b

        assert c(x) == a(x) * b(x)

    def test_mul_throws_errors(self):

        a = Sampler()

        with raises(TypeError) as err:
            a * 2

        assert 'supported between Sampler objects' in str(err.value)


@given(x=value, y=value)
def test_sampling_of_f(x, y):

    # Construct an interpolation of the two
    def f(t):
        return (1 - t)*x + t*y

    s = Sampler(f)

    assert s._data[0] == x
    assert s._data[-1] == y


@given(num_points=numpoints)
def test_sampler_getitem(num_points):

    s = Sampler(num_points=(num_points + 10))

    assert s[0] == 0
    assert s[-1] == 1
    assert len(s[:-10]) == num_points
