class StyloError(Exception):
    """An exception to group all stylo related errors under."""

    pass


class MissingDependencyError(StyloError):
    """An exception to represent a missing dependency."""

    def __init__(self, extra):

        message = "You are missing dependencies required to use this feature."
        message += " Please run `pip install stylo[{}]` to install them"

        super().__init__(message.format(extra))
