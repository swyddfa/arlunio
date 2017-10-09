import unittest.mock as mock
import numpy as np


import pytest
from pytest import raises, fixture
from hypothesis import given, assume
from hypothesis.strategies import composite, integers,\
                                  tuples, lists, floats,\
                                  text


from stylo.interpolate import Channel

# Some settings
DATA_MAX = 1.0
DATA_MIN = 0.0
DATA_LENGTH = 512

# Some strategy definitions
index = integers(min_value=0, max_value=(DATA_LENGTH - 1))
pveint = integers(min_value=1, max_value=2*DATA_LENGTH)
real = floats(min_value=-1e6, max_value=1e6)


@composite
def data(draw):
    length = draw(pveint)
    start = draw(real)
    stop = draw(real)

    return np.linspace(start, stop, length)


segment = tuples(pveint, data())


# Some fixtures
@fixture
def channel():
    # Just a 'Vanilla' Channel with no extras
    return Channel()


@fixture
def channel_cycle():
    # An empty channel with Cycle enabled
    c = Channel()
    c._cycle = True

    return c


@fixture
def channel_data():
    # A channel with some example data
    c = Channel()
    c._segments = 1     # Pretend this data is real
    c._data = np.linspace(DATA_MIN, DATA_MAX, DATA_LENGTH)

    return c


@fixture
def channel_data_cycle():
    # A channel with cycled example data
    c = Channel()
    c._cycle = True
    c._segments = 1     # Pretend that the data is real
    c._data = np.linspace(DATA_MIN, DATA_MAX, DATA_LENGTH)

    return c


class TestProperties(object):

    def test_data_property(self):

        channel = Channel()

        # By default it should be empty
        assert (channel.data == np.array([])).all()

        # And it should be READ ONLY!
        with raises(AttributeError) as err:
            channel.data = 1

        assert 'can\'t set attribute' in str(err.value)


    def test_cycle_property(self):

        channel = Channel()

        # By default it should be false
        assert channel.cycle is False

        # We should be able to set it
        channel.cycle = True
        assert channel.cycle is True

        # If we try to set it to anything except a bool
        # then it should complain
        with raises(TypeError) as err:
            channel.cycle = 42

        assert 'must be a bool' in str(err.value)

        # We should also check that the old value was preserved
        assert channel.cycle is True

    @given(name=text(average_size=32))
    def test_name_property(self, name):

        channel = Channel()

        # By default this should be the empty string
        assert channel.name is ''

        # We should be able to change that
        channel.name = name
        assert channel.name == name

        # But only to a string
        with raises(TypeError) as err:
            channel.name = True

        assert 'must be a str' in str(err.value)

        # We should also check that the old value was preserved
        assert channel.name == name

    @given(fps=pveint)
    @mock.patch.object(Channel, '_construct')
    def test_fps_property_with_int(self, mock_construct, fps):

        channel = Channel()

        # The construct method should already have been called
        assert mock_construct.call_count == 1

        # By default this should be 25
        assert channel.FPS == 25

        # We should be able to change this
        channel.FPS = fps
        assert channel.FPS == fps

        # But changing this should call the _construct method
        assert mock_construct.call_count == 2

    @given(fps=pveint)
    @mock.patch.object(Channel, '_construct')
    def test_fps_property_with_bad_values(self, mock_construct, fps):

        channel = Channel()

        # FPS should be a default value of 25
        assert channel.FPS == 25

        # The construct method should have already been called
        assert mock_construct.call_count == 1

        # Try and change the FPS property to something
        # other than an int
        with raises(TypeError) as err:
            channel.FPS = 'a string!'

        assert 'must be an int' in str(err.value)

        # The value should be unchanged
        assert channel.FPS == 25

        # The construct method should NOT have been called again
        assert mock_construct.call_count == 1

        # Similarly there should be an error if we try a negative
        # FPS
        with raises(ValueError) as err:
            channel.FPS = -fps

        assert 'must be larger than 0' in str(err.value)
        assert channel.FPS == 25
        assert mock_construct.call_count == 1

    @given(segments=lists(segment, average_size=12))
    @mock.patch.object(Channel, '_construct')
    def test_segments_property(self, mock_construct, segments):

        channel = Channel()

        # By default it should be the empty list and the construct
        # method should've been called
        assert channel.segments == []
        assert mock_construct.call_count == 1

        # We should be able to change this
        channel.segments = segments

        mask = channel.segments == sorted(segments, key=lambda x: x[0])

        if isinstance(mask, (bool,)):
            assert mask
        else:
            assert all(mask)

        # And the construct function should be called again
        assert mock_construct.call_count == 2

    @mock.patch.object(Channel, '_construct')
    def test_segments_property_with_bad_values(self, mock_construct):

        channel = Channel()
        assert mock_construct.call_count == 1

        # The segments property must enforce the correct
        # structure
        with raises(TypeError) as err:
            channel.segments = 128

        assert 'must be a list' in str(err.value)

        # The old value must be unchanged and the construct
        # function not called
        assert channel.segments == []
        assert mock_construct.call_count == 1

        # Each item must be a tuple
        with raises(TypeError) as err:
            channel.segments = [(0, [1, 2, 3]), 1.2]

        assert 'must be a tuple' in str(err.value)
        assert channel.segments == []
        assert mock_construct.call_count == 1

        # Each tuple must be the right length
        with raises(TypeError) as err:
            channel.segments = [(0, [1, 2, 3]), (0.2,)]

        assert 'length 2' in str(err.value)
        assert channel.segments == []
        assert mock_construct.call_count == 1

        # The first entry must be a non negative integer
        with raises(TypeError) as err:
            channel.segments = [(0, [1, 2, 3]), (0.2, [])]

        assert 'must be an integer' in str(err.value)
        assert channel.segments == []
        assert mock_construct.call_count == 1

        with raises(ValueError) as err:
            channel.segments = [(0, [1, 2, 3]), (-2, [])]

        assert 'cannot be negative' in str(err.value)
        assert channel.segments == []
        assert mock_construct.call_count == 1

        # Finally the second entry must be an iterable
        with raises(TypeError) as err:
            channel.segments = [(0, [1, 2, 3]), (12, 128)]

        assert 'must be iterable' in str(err.value)
        assert channel.segments == []
        assert mock_construct.call_count == 1


class TestGetItem(object):

    @given(i=index)
    def test_with_index_nodata_nocycle(self, channel, i):

        # When a channel has no segments it should generate fake
        # data to make it look like it is zero everywhere
        assert channel[i] == 0.0
        assert channel[-i] == 0.0

    @given(i=index)
    def test_with_index_nodata_cycle(self, channel_cycle, i):

        # In this case cycle being set should not make a difference
        assert channel_cycle[i] == 0.0
        assert channel_cycle[-i] == 0.0

    @given(i=index, offset=pveint)
    def test_with_slice_nodata_nocycle(self, channel, i, offset):
        # When a channel has no segments it should generate
        # fake data to make it look like it is zero everywhere
        res = channel[slice(i, i + offset)]
        assert len(res) == offset
        assert (res == 0.0).all()

    @given(i=index, offset=pveint)
    def test_with_slice_nodata_cycle(self, channel_cycle, i, offset):

        # In this case cycle being set should not make a difference
        res = channel_cycle[slice(i, i + offset)]
        assert len(res) == offset
        assert (res == 0.0).all()

    @given(i=index)
    def test_with_inner_index_data_nocycle(self, channel_data, i):

        # An index within the data should return the data itself
        assert channel_data[i] == \
               np.linspace(DATA_MIN, DATA_MAX, DATA_LENGTH)[i]

    @given(i=index)
    def test_with_later_index_data_nocycle(self, channel_data, i):

        # If we're not cycling the data then any index after the data
        # should return the final value
        assert channel_data[DATA_LENGTH + i] == DATA_MAX

    @given(i=index)
    def test_with_earlier_index_data_nocycle(self, channel_data, i):
        # Negative indices should return the initial value of the data
        assert channel_data[-i] == DATA_MIN

    @given(i=index)
    def test_with_inner_index_data_cycle(self, channel_data_cycle, i):

        # An index within the data should return the data itself
        assert channel_data_cycle[i] == \
               np.linspace(DATA_MIN, DATA_MAX, DATA_LENGTH)[i]

    @given(i=index)
    def test_with_later_index_data_cycle(self, channel_data_cycle, i):
        # An index after the data should return the value of i mod length
        assert channel_data_cycle[DATA_LENGTH + i] == \
               np.linspace(DATA_MIN, DATA_MAX, DATA_LENGTH)[i]

    @given(i=index)
    def test_with_earlier_index_data_cycle(self, channel_data_cycle, i):
        assume(i > 0)

        # The same for any negative indices
        assert channel_data_cycle[-i] == \
               np.linspace(DATA_MIN, DATA_MAX,
                           DATA_LENGTH)[DATA_LENGTH - i]

    @given(i=index, offset=pveint)
    def test_with_inner_bounded_slice_data_nocycle(self, channel_data,
                                                   i, offset):
        assume(i + offset < DATA_LENGTH - 1)

        # Slices within the data should return the data itself
        res = channel_data[slice(i, i + offset)]
        assert len(res) == offset

        mask = res == np.linspace(DATA_MIN, DATA_MAX,
                                  DATA_LENGTH)[slice(i, i + offset)]
        assert mask.all()

    @given(i=index)
    def test_with_inner_boundbelow_slice_data_nocycle(self, channel_data, i):

        # Slices that are unbounded should stop at the end of the real data
        res = channel_data[slice(i, None)]
        assert len(res) == DATA_LENGTH - i

        mask = res == np.linspace(DATA_MIN, DATA_MAX,
                                  DATA_LENGTH)[slice(i, None)]
        assert mask.all()

    @given(i=index)
    def test_with_inner_boundedabove_slice_data_nocycle(self, channel_data, i):

        # Slices that are unbounded should simply start at the beginning
        # of the real data
        res = channel_data[slice(None, i)]
        assert len(res) == i

        mask = res == np.linspace(DATA_MIN, DATA_MAX,
                                  DATA_LENGTH)[slice(None, i)]
        assert mask.all()

    def test_with_unbounded_slice_data_nocycle(self, channel_data):

        # Unbounded slice should simply return the data
        res = channel_data[slice(None, None)]
        assert len(res) == DATA_LENGTH

        mask = res == np.linspace(DATA_MIN, DATA_MAX, DATA_LENGTH)
        assert mask.all()

    @given(offset=pveint)
    def test_with_later_slice_data_nocycle(self, channel_data, offset):

        # When the slice extends over the end of the data (with no cycling)
        # it should return the final value repeated
        res = channel_data[slice(DATA_LENGTH, DATA_LENGTH + offset)]
        assert len(res) == offset
        assert (res == 1.0).all()

    @given(offset=pveint)
    def test_with_earlier_slice_data_nocycle(self, channel_data, offset):

        # Similarly if the slice start before the data it should
        # return the initial value repeated
        res = channel_data[slice(0 - offset, 0)]
        assert len(res) == offset
        assert (res == 0.0).all()

    @given(i=index, offset=pveint)
    def test_with_inner_bounded_slice_data_cycle(self, channel_data_cycle,
                                                 i, offset):
        assume(i + offset < DATA_LENGTH)

        # When a channel has segments, a slice fully within the
        # data should return the data itself
        res = channel_data_cycle[slice(i, i + offset)]
        assert len(res) == offset

        mask = res == np.linspace(DATA_MIN, DATA_MAX,
                                  DATA_LENGTH)[slice(i, i + offset)]
        assert mask.all()

    @given(i=index)
    def test_with_inner_boundbelow_slice_data_cycle(self,
                                                    channel_data_cycle, i):

        # Unbounded slices should stop at the end of the real data
        res = channel_data_cycle[slice(i, None)]
        assert len(res) == DATA_LENGTH - i

        mask = res == np.linspace(DATA_MIN, DATA_MAX,
                                  DATA_LENGTH)[slice(i, None)]
        assert mask.all()

    @given(i=index)
    def test_with_inner_boundabove_slice_data_cycle(self,
                                                    channel_data_cycle, i):

        # Unbounded slices should just start at the beginning of the data
        res = channel_data_cycle[slice(None, i)]
        assert len(res) == i

        mask = res == np.linspace(DATA_MIN, DATA_MAX,
                                  DATA_LENGTH)[slice(None, i)]
        assert mask.all()

    @given(offset=pveint)
    def test_with_later_slice_data_cycle(self, channel_data_cycle, offset):

        # When the slice extends over the end of the data it should
        # return the data, repeated
        res = channel_data_cycle[slice(DATA_LENGTH, DATA_LENGTH + offset)]
        assert len(res) == offset

        testarr = np.unique(res)
        testoff = min(offset, DATA_LENGTH)

        mask = testarr == np.linspace(DATA_MIN, DATA_MAX,
                                      DATA_LENGTH)[slice(0, testoff)]
        assert mask.all()

    @given(offset=pveint)
    def test_with_earlier_slice_data_cycle(self, channel_data_cycle, offset):

        # When the mask starts before the data it should return the
        # data, repeated
        res = channel_data_cycle[slice(-offset, 0)]
        assert len(res) == offset

        testarr = np.unique(res)
        testoff = min(offset, DATA_LENGTH)

        mask = testarr == np.linspace(DATA_MIN, DATA_MAX,
                                  DATA_LENGTH)[slice(DATA_LENGTH - testoff, None)]
        assert mask.all()

    def test_throws_type_error(self, channel):

        for val in [1.0, 'str', {}, []]:
            with raises(TypeError) as err:
                channel[val]

            assert 'must be an int' in str(err.value)


class TestConstruct(object):

    def test_with_no_data(self):

        channel = Channel()

        # With no data, the internal data should be the empty
        # list and len should report zero
        assert len(channel) == 0
        assert (channel.data == np.array([])).all()

    @given(s=segment)
    def test_with_single_segment(self, s):

        frame = s[0]
        data = s[1]

        channel = Channel([s])
        cdata = channel.data

        assert len(channel) == frame + len(data)
        mask = cdata[:frame] == [data[0] for _ in range(frame)]
        assert mask.all()

        mask = cdata[frame:] == data
        assert mask.all()

    @pytest.mark.slow
    @given(intervals=lists(data(), average_size=12))
    def test_with_many_sequential_intervals(self, intervals):

        segments = []
        indices = []
        frame = 0

        for interval in intervals:
            segments.append((frame, interval))
            frame += len(interval)
            indices.append(frame)

        length = sum(map(len, intervals))

        channel = Channel(segments)

        assert len(channel) == length

        start_index = 0

        for i in range(len(indices)):
            print("Index: {}".format(indices[i]))
            print("Channel: {}".format(channel[:indices[i]]))
            print("Interval: {}".format(intervals[i]))

            mask = channel[start_index:indices[i]] == intervals[i]
            start_index = indices[i]
            assert mask.all()


    @pytest.mark.slow
    @given(intervals=lists(data(), average_size=12),
           offsets=lists(pveint, min_size=1, average_size=12))
    def test_with_many_offset_intervals(self, intervals, offsets):

        assume(len(intervals) == len(offsets))

        segments = []
        indices = []
        frame = 0

        for offset, interval in zip(offsets, intervals):
            frame += offset
            indices.append(frame)
            segments.append((frame, interval))
            frame += len(interval)
            indices.append(frame)

        length = sum(map(len, intervals)) + sum(offsets)

        channel = Channel(segments)
        assert len(channel) == length

        # TODO: Test that all the right values show up in the right
        # places, I can't think of a clean way to do this right now
