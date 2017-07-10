import pytest
from hypothesis import given
from hypothesis.strategies import tuples, lists, floats,\
                                  booleans, integers, text,\
                                  one_of

from mage.motion import Driver

# Some useful strategies
frameno = integers(min_value=-1e6, max_value=1e6)
realtime = floats(min_value=--1000, max_value=1000)
time = one_of(frameno, realtime)
value = floats(min_value=-1e6, max_value=1e6)
keyframe = tuples(time, value)
fps = integers(min_value=1, max_value=500)


def test_init_defaults():

    d = Driver()

    assert d.FPS == d._FPS
    assert d.FPS == 25

    assert d.cycle == d._cycle
    assert d.cycle is False

    assert d.name == d._name
    assert d.name == ''

    assert d.keyframes == d._keys
    assert d.keyframes == [(0.0, 0), (1.0, 1)]

    assert (d.frames == d._data).all()
    assert len(d.frames) == 25
    assert d.frames[0] == 0
    assert d.frames[-1] == 1


@given(FPS=fps)
def test_FPS_property(FPS):

    d = Driver(FPS=FPS)

    assert d.FPS == FPS

    with pytest.raises(TypeError) as err:
        d.FPS = 'string'

    assert 'must be an integer' in str(err.value)

    with pytest.raises(ValueError) as err:
        d.FPS = -FPS

    assert 'must be a positive' in str(err.value)


@given(cycle=booleans())
def test_cycle_property(cycle):

    d = Driver(cycle=cycle)

    assert d.cycle == cycle

    with pytest.raises(TypeError) as err:
        d.cycle = ('bob', 'trudy')

    assert 'must be a boolean' in str(err.value)


@given(name=text())
def test_name_property(name):

    d = Driver(name=name)

    assert d.name == name

    with pytest.raises(TypeError) as err:
        d.name = 123

    assert 'must be a string' in str(err.value)


@given(keyframes=lists(keyframe, min_size=2, max_size=12))
def test_keyframes_properties(keyframes):

    d = Driver(keyframes=keyframes)

    assert d.keyframes == keyframes

    with pytest.raises(AttributeError) as err:
        d.keyframes = keyframes[:-1]

    assert "can't set attribute" in str(err.value)


@given(keyframes=lists(keyframe, min_size=2, max_size=12))
def test_sorted_keys(keyframes):

    d = Driver(keyframes=keyframes)

    keys = d._sorted_keys()

    # We shouldn't lose or gain any keyframes
    assert len(keys) == len(keyframes)

    times = [it[0] for it in keys]

    # All time codes should now be integers
    assert all([isinstance(time, (int,)) for time in times])

    # The times should already be sorted
    assert times == sorted(times)

    ## How to test the time conversion??


@given(FPS=fps, index=frameno)
def test_get_single_frameno(FPS, index):

    drive = Driver(FPS=FPS)

    # If index < 0 we should be seeing the value zero
    if index < 0:
        assert drive._get_single(index) == 0
        return

    # If index > fps then we should be seeing the value one
    if index > FPS:
        assert drive._get_single(index) == 1
        return

    # Otherwise, some value between 0 and 1 will driveo
    assert 0 <= drive._get_single(index)
    assert 1 >= drive._get_single(index)


@given(FPS=fps, index=frameno)
def test_get_single_frameno_cycled(FPS, index):

    drive = Driver(FPS=FPS, cycle=True)
    length = len(drive._data)

    # If index mod length = 0, we should see the value
    # zero
    if index % length == 0:
        assert drive._get_single(index) == 0
        return

    # If index mod length = (length - 1), we should see the value 1
    if index % length == (length - 1):
        assert drive._get_single(index) == 1
        return

    # Otherwise we should see a value in the range 0 - 1
    assert 0 <= drive._get_single(index)
    assert 1 >= drive._get_single(index)


@given(FPS=fps, index=frameno)
def test_getitem_frameno(FPS, index):

    drive = Driver(FPS=FPS)

    # If index < 0 we should be seeing the value zero
    if index < 0:
        assert drive[index] == 0
        return

    # If index > fps then we should be seeing the value one
    if index > FPS:
        assert drive[index] == 1
        return

    # Otherwise, some value between 0 and 1 will driveo
    assert 0 <= drive[index]
    assert 1 >= drive[index]


@given(FPS=fps, index=frameno)
def test_getitem_frameno_cycled(FPS, index):

    drive = Driver(FPS=FPS, cycle=True)
    length = len(drive._data)

    # If index mod length = 0, we should see the value
    # zero
    if index % length == 0:
        assert drive[index] == 0
        return

    # If index mod length = (length - 1), we should see the value 1
    if index % length == (length - 1):
        assert drive[index] == 1
        return

    # Otherwise we should see a value in the range 0 - 1
    assert 0 <= drive[index]
    assert 1 >= drive[index]


@given(FPS=fps, index=realtime)
def test_getitem_realtime(FPS, index):

    drive = Driver(FPS=FPS)

    # If index < 0, we should see the value zero
    if index < 0:
        assert drive[index] == 0
        return

    # If index > 1 we should see the value one
    if index > 1:
        assert drive[index] == 1
        return

    # Otherwise we should see a value between zero and 1
    assert 0 <= drive[index]
    assert 1 <= drive[index]


@given(FPS=fps, index=realtime)
def test_getitem_realtime_cycled(FPS, index):

    drive = Driver(FPS=FPS, cycle=True)

    # If index is a whole number we should see the value zero
    if index % 1 == 0:
        assert drive[index] == 0

    # Otherwise we should see a value between 0 and 1
    assert 0 <= drive[index]
    assert 1 >= drive[index]
