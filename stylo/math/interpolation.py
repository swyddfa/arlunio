def lerp(a, b):
    """Return a function that will linearly interpolate between :code:`a` and :code:`b`.

    The returned function will take the value :code:`a` when passed the value :code:`0`
    and will increase/decrease linearly to the value :code:`b`, taking that value at the
    point :code:`1`.

    :param float a: The value the function should take at :code:`0`
    :param float b: The value the function should take at :code:`1`
    """

    def s(t):
        return (1 - t) * a + t * b

    return s
