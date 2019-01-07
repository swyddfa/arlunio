class StyloError(Exception):
    """An exception to group all stylo related errors under."""

    pass


class MissingDependencyError(StyloError):
    """An exception to represent a missing dependency."""

    pass
