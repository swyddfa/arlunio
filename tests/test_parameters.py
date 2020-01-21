import arlunio as ar


def test_use_parameter_as_tag():
    """Ensure that the parameter decorator can be used as a simple tag."""

    @ar.parameter
    def Param(width, height):
        return width

    p = Param()
    assert p(4, 2) == 4


def test_use_parameter_as_function():
    """Ensure that the parameter decorator can be used as a function."""

    @ar.parameter()
    def Param(width, height):
        return height

    p = Param()
    assert p(4, 2) == 2


def test_parameter_constant():
    """Ensure that we can define as constant parameter."""

    @ar.parameter
    def Constant():
        return 1

    const = Constant()
    assert const(10, 10) == 1
