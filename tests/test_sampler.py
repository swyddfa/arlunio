from hypothesis import given
from hypothesis.strategies import floats, integers
from pytest import raises

from stylo.interpolate import Sampler

# Some useful types
numpoints = integers(min_value=2, max_value=1000)
value = floats(min_value=-1e6, max_value=1e6)

def test_defaults():

    s = Sampler()

    assert s.num_points == 25
    assert s.name == 'Sampled function:'
    assert callable(s.f)


@given(num_points=numpoints)
def test_num_points_prop(num_points):

    s = Sampler(num_points=num_points)
    assert s.num_points == num_points

    with raises(TypeError) as err:
        s.num_points = 'string'

    assert 'must be an integer' in str(err.value)

    with raises(ValueError) as err:
        s.num_points = -num_points

    assert 'be larger than 2' in str(err.value)


@given(num_points=numpoints)
def test_num_points_affect_data_len(num_points):

    s = Sampler(num_points=num_points)
    assert len(s._data) == num_points

@given(x=value, y=value)
def test_sampling_of_f(x, y):

    # Construct an interpolation of the two
    def f(t):
        return (1 - t)*x + t*y

    s = Sampler(f)

    assert s._data[0] == x
    assert s._data[-1] == y


@given(x=value)
def test_sampler_is_callable(x):

    s = Sampler()
    assert s(x) == x

    def squared(y):
        return y * y

    s.f = squared
    assert s(x) == x * x


@given(num_points=numpoints)
def test_sampler_getitem(num_points):

    s = Sampler(num_points=(num_points + 10))

    assert s[0] == 0
    assert s[-1] == 1
    assert len(s[:-10]) == num_points
