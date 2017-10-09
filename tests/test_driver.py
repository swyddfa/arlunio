import pytest
import numpy as np

from stylo.interpolate import Driver, Channel

from pytest import raises
from hypothesis import given, assume
from hypothesis.strategies import text, lists, integers,\
                                  composite, floats


# Some useful strategies
names = text(min_size=1, average_size=12)
pveint = integers(min_value=1, max_value=1024)
real = floats(min_value=-1e6, max_value=1e6)


@composite
def data(draw):
    length = draw(pveint)
    start = draw(real)
    stop = draw(real)

    return (0, np.linspace(start, stop, length))


class TestProperties(object):

    @given(c_names=lists(names, average_size=4))
    def test_channels_property(self, c_names):
        assume(len(set(c_names)) == len(c_names))

        driver = Driver()

        for name in c_names:
            driver.add_channel(name)

        # This should simply return a list of the available
        # channels
        assert driver.channels == c_names

        # This attribute should be read only
        with raises(AttributeError) as err:
            driver.channels = 2

        assert 'can\'t set attribute' in str(err.value)

    @given(fps=pveint)
    def test_fps_property_with_good_values(self, fps):

        driver = Driver()

        # By default fps should be 25
        assert driver.FPS == 25

        # We should be able to change this
        driver.FPS = fps
        assert driver.FPS == fps

    @given(fps=pveint)
    def test_fps_property_with_bad_values(self, fps):

        driver = Driver()

        with raises(TypeError) as err:
            driver.FPS = 'a str'

        assert 'must be an integer' in str(err.value)

        with raises(ValueError) as err:
            driver.FPS = -fps

        assert 'must be larger than zero' in str(err.value)

    @pytest.mark.slow
    @given(segments=lists(data(), min_size=1, average_size=4),
           names=lists(names, min_size=1, average_size=4))
    def test_len_property(self, names, segments):

        assume(len(names) == len(set(names)))
        assume(len(segments) == len(names))
        lengths = []

        driver = Driver()

        for name, data in zip(names, segments):
            driver.add_channel(name, segments=[data])
            lengths.append(len(data[1]))

        # When we ask for the length of the driver, it should be
        # be equal to the longest of its component channels
        assert len(driver) == max(lengths)


class TestChannelManagement(object):

    @given(name=names)
    def test_adding_new_channel(self, name):

        driver = Driver()
        driver.add_channel(name, FPS=50, cycle=True)

        # The name should have been added into the internal record
        # of channels
        assert name in driver._channels

        # We should now be able to access the Channel object
        # directly
        assert isinstance(driver.__getattribute__(name), (Channel,))

        # It should also have respected its own __init__ arguments
        assert driver.__getattribute__(name).FPS == 50
        assert driver.__getattribute__(name).cycle

    @given(name=names)
    def test_adding_existing_channel(self, name):

        channel = Channel()
        driver = Driver()

        driver.add_channel(name, channel=channel)
        assert name in driver._channels
        assert isinstance(driver.__getattribute__(name), (Channel,))

        # By default the Channel should be added with a zero offset.
        assert driver._channels[name] == 0

    @given(name=names)
    def test_add_channel_throws_errors(self, name):

        driver = Driver()

        # Name should only be a str
        with raises(TypeError) as err:
            driver.add_channel(1)

        assert 'must be a string' in str(err.value)

        # And the string cannot be empty
        with raises(ValueError) as err:
            driver.add_channel('')

        assert 'cannot be the empty string' in str(err.value)

        driver.add_channel(name)

        # Adding a new channel with an exisiting name should throw an
        # error
        with raises(RuntimeError) as err:
            driver.add_channel(name)

        assert 'already exists' in str(err.value)

        with raises(TypeError) as err:
            driver.add_channel('new name', 3)

        assert 'Expected Channel instance' in str(err.value)

    @given(name=names)
    def test_deleting_channel(self, name):

        driver = Driver()
        driver.add_channel(name)

        assert name in driver._channels
        assert isinstance(driver.__getattribute__(name), (Channel,))

        driver.del_channel(name)

        assert name not in driver._channels

        with raises(AttributeError):
            driver.__getattribute__(name)

    @given(name=names)
    def test_del_channel_throws_errors(self, name):

        driver = Driver()

        with raises(TypeError) as err:
            driver.del_channel(2)

        assert 'by a string' in str(err.value)

        with raises(RuntimeError) as err:
            driver.del_channel(name)

        assert 'does not exist' in str(err.value)


class TestGetItem(object):

    @given(name=names)
    def test_get_channel_by_name(self, name):

        driver = Driver()
        driver.add_channel(name)

        channel = driver[name]

        assert isinstance(channel, (Channel,))
