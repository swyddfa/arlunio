import pytest
from hypothesis import given
from hypothesis.strategies import integers

from stylo.time import Timeline


time = integers(min_value=1)


@pytest.mark.time
class TestTimeline:
    """Tests for the :code:`Timeline` class"""

    def test_init_defaults(self):
        """Ensure that sensible defaults are chosen if no arguments given."""

        timeline = Timeline()
        assert timeline.framecount == 0
        assert timeline.duration == 0
        assert timeline.fps == 25

    @given(seconds=time)
    def test_duration_is_framecount(self, seconds):
        """Ensure that when the frames per second is one, that the framecount matches
        the duration."""

        timeline = Timeline(seconds=seconds, fps=1)
        assert timeline.framecount == seconds
        assert timeline.duration == seconds

    @given(hours=time)
    def test_duration_calc_with_hours(self, hours):
        """Ensure that we can specify the duration in hours."""

        timeline = Timeline(hours=hours)
        assert timeline.duration == hours * 60 * 60

    @given(minutes=time)
    def test_duration_calc_with_minutes(self, minutes):
        """Ensure that we can specifiy the duration in minutes."""

        timeline = Timeline(minutes=minutes)
        assert timeline.duration == minutes * 60

    @given(seconds=time)
    def test_duration_calc_with_seconds(self, seconds):
        """Ensure that we can specify the duration in seconds."""

        timeline = Timeline(seconds=seconds)
        assert timeline.duration == seconds

    def test_build_filename(self):
        """Ensure that we can generate appropriate filnames to use to save image
        sequences."""

        timeline = Timeline(seconds=10)
        timeline._build_filename("my/animation/frame.png")

        assert timeline._filename == "my/animation/frame-{:03d}.png"

    def test_timeline_main(self):
        """Ensure that we can declare a main function and render it."""

        timeline = Timeline(seconds=10)

        class Counter:
            def __init__(self):
                self.count = 0

        counter = Counter()

        @timeline.main
        def animation(f, t):
            counter.count += 1

        timeline.render()
        assert counter.count == 250
