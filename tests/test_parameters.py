import arlunio as ar
import py.test


@py.test.fixture()
def collection():
    """An empty collection for each test case."""
    return ar.Collection()


def test_use_parameter_as_tag():
    """Ensure that the parameter decorator can be used as a simple tag."""

    @ar.parameter
    def z123_(width, height):
        return width

    p = z123_()
    assert p(4, 2) == 4


def test_use_parameter_as_function(collection):
    """Ensure that the parameter decorator can be used as a function."""

    @ar.parameter(collection=collection)
    def Param(width, height):
        return height

    p = Param()
    assert p(4, 2) == 2


def test_parameter_default_collection():
    """Ensure that if we don't specify a collection the parameter will be added to the
    default one."""

    @ar.parameter
    def x123_P():
        return 0

    assert x123_P == ar.P.x123_P


def test_parameter_with_collection():
    """Ensure that if a collection is given the parameter will be added to the given
    collection."""

    my_collection = ar.Collection()

    @ar.parameter(collection=my_collection)
    def Param(width):
        return width

    with py.test.raises(AttributeError) as err:
        ar.P.Param

    assert "Param" in str(err.value)
    assert my_collection.Param == Param


def test_parameter_constant(collection):
    """Ensure that we can define as constant parameter."""

    @ar.parameter(collection=collection)
    def Constant():
        return 1

    const = Constant()
    assert const(10, 10) == 1


def test_parameter_width_only(collection):
    """Ensure that we can define a parameter with respect to width only."""

    @ar.parameter(collection=collection)
    def Width(width):
        return width + 1

    w = Width()
    assert w(100, 2) == 101


def test_parameter_height_only(collection):
    """Ensure that we can define a parameter with respect to height only."""

    @ar.parameter(collection=collection)
    def Height(height):
        return height - 1

    h = Height()
    assert h(2, 100) == 99


def test_parameter_attributes(collection):
    """Ensure that we can define a parameter that takes a number of attributes."""

    @ar.parameter(collection=collection)
    def Param(width, height, *, offset=0):
        return (width + height) - offset

    p = Param()
    assert p(1, 1) == 2

    q = Param(offset=2)
    assert q(1, 1) == 0
