import inspect
from uuid import uuid4


def get_parameters(f):
    return list(inspect.signature(f).parameters.keys())


class MessageBus:
    """A class that is used behind the scenes to coordinate events and timings of
    animations.
    """

    def __init__(self):
        self.subs = {}

    def new_id(self):
        """Use this to get a name to use for your events."""
        return str(uuid4())

    def register(self, event, obj):
        """Register to receive notifications of an event.

        :param event: The name of the kind of event to receive
        :param obj: The object to receive that kind of message.
        """

        if event not in self.subs:
            self.subs[event] = [obj]
            return

        self.subs[event].append(obj)

    def send(self, event, **kwargs):
        """Send a message to whoever may be listening."""

        if event not in self.subs:
            return

        for obj in self.subs[event]:

            params = get_parameters(obj)
            values = {k: v for k, v in kwargs.items() if k in params}

            obj(**values)


_message_bus = MessageBus()


def get_message_bus():
    """A function that returns an instance of the message bus to ensure everyone uses
    the same instance."""
    return _message_bus
