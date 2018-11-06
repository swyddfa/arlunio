from stylo.utils import get_message_bus


class Clock:
    """This manages all the ticking etc."""

    def __init__(self, fps=25):
        self.fps = fps
        self.timedelta = 1 / fps
        self.bus = get_message_bus()

        self.time = 0
        self.tick = 0

        self.event_id = self.bus.new_id()

    def on_tick(self, obj):
        self.bus.register(self.event_id, obj)

    def __call__(self):
        self.tick += 1
        self.time += self.timedelta

        self.bus.send(self.event_id, f=self.tick, t=self.time)
