import inspect

from typing import Any

import arlunio as ar
import py.test


def test_definition_name():
    """Ensure that the returned definition keeps the name of the decorated function."""

    @ar.definition
    def Circle():
        return 1

    assert Circle.__name__ == "Circle"


def test_definition_module():
    """Ensure that the returned definition reports its module as the one it was defined
    in"""

    @ar.definition()
    def Circle():
        pass

    assert Circle.__module__ == "tests.test_core"


def test_use_definition_as_tag():
    """Ensure that the definition decorator can be used as a simple tag."""

    @ar.definition
    def z123_(width, height):
        return width

    p = z123_()
    assert p(4, 2) == 4


def test_use_definition_as_function():
    """Ensure that the definition decorator can be used as a function."""

    @ar.definition()
    def Param(width, height):
        return height

    p = Param()
    assert p(4, 2) == 2


def test_definition_constant():
    """Ensure that we can define as constant definition."""

    @ar.definition()
    def Constant():
        return 1

    const = Constant()
    assert const(10, 10) == 1


def test_definition_width_only():
    """Ensure that we can define a definition with respect to width only."""

    @ar.definition()
    def Width(width):
        return width + 1

    w = Width()
    assert w(100, 2) == 101


def test_definition_height_only():
    """Ensure that we can define a definition with respect to height only."""

    @ar.definition()
    def Height(height):
        return height - 1

    h = Height()
    assert h(2, 100) == 99


def test_definition_attributes():
    """Ensure that we can define a definition that takes a number of attributes."""

    @ar.definition()
    def Param(width, height, *, offset=0):
        return (width + height) - offset

    p = Param()
    assert p(1, 1) == 2

    q = Param(offset=2)
    assert q(1, 1) == 0


def test_definition_attribute_validation():
    """Ensure that if an attribute is given a type hint we can perform some basic
    validation on it."""

    @ar.definition()
    def Param(width, height, *, a: int = 0):
        pass

    with py.test.raises(TypeError):
        Param(a="string")


def test_definition_produces_any():
    """Ensure that a definition without a return annotation reports its return type as
    :code:`Any`"""

    @ar.definition()
    def Param():
        pass

    assert Param.produces() == Any
    assert Param().produces() == Any


def test_definition_produces():
    """Ensure that a definition reports what type it returns as declared by its return
    annotation"""

    @ar.definition()
    def Param() -> int:
        return 1

    assert Param.produces() == int
    assert Param().produces() == int


def test_derived_definition():
    """Ensure that we can derive a definition that's based on other definitions."""

    @ar.definition()
    def Adder(width, height):
        return height + width

    @ar.definition()
    def Subber(a: Adder):
        return a - 2

    s = Subber()
    assert s(1, 1) == 0
    assert s(1, 2) == 1


def test_derived_definition_checks_input_annotations():
    """Ensure that any inputs that are not a base definition or annotated are complained
    about."""

    with py.test.raises(TypeError) as err:

        @ar.definition()
        def Parameter(width, height, x):
            return width * height - x

    assert "Unknown input 'x'" in str(err.value)


def test_derived_definition_checks_input_annotation_type():
    """Ensure that any inputs that are annotated with a class that's not a Parameter are
    compained about."""

    with py.test.raises(TypeError) as err:

        @ar.definition()
        def Parameter(width, height, x: int):
            return width * height - x

    assert "Invalid input 'x', type 'int' is not a Definition" in str(err.value)


def test_derived_definition_exposes_properties():
    """Ensure that any properties on base definitions are exposed on the derived
    property."""

    @ar.definition()
    def Base(width, height, *, offset=0):
        return offset

    @ar.definition()
    def Derived(b: Base, *, start=1):
        return start - b

    d = Derived()
    d(1, 1) == 1

    d = Derived(start=5, offset=-1)
    d(1, 1) == 6


def test_derived_definition_exposes_base_definitions():
    """Ensure that any base definitions are available to be inspected."""

    @ar.definition()
    def Base(width, height):
        return 2

    assert Base.definitions == {
        "width": inspect.Parameter.empty,
        "height": inspect.Parameter.empty,
    }

    @ar.definition()
    def Derived(width, base: Base):
        return 4

    assert Derived.definitions == {"width": inspect.Parameter.empty, "base": Base}


def test_derived_definition_attributes_property():
    """Ensure that the attributes property exposes all available attributes on the
    definition."""

    @ar.definition
    def Base(width, height, *, a=1, b=2):
        return 3

    assert Base().attributes == {"a": 1, "b": 2}

    @ar.definition()
    def Derived(base: Base, *, b=3, d=4):
        return 5

    assert Derived().attributes == {"a": 1, "b": 3, "d": 4}


def test_derived_definition_attribs_property():
    """Ensure that the attribs property only exposes the attributes that are directly
    defined on the definition."""

    @ar.definition
    def Base(width, height, *, a=1, b=2):
        return 3

    assert Base().attribs == {"a": 1, "b": 2}

    @ar.definition
    def Derived(base: Base, *, b=3, d=4):
        return 5

    assert Derived().attribs == {"b": 3, "d": 4}


def test_derived_definition_eval_width_height():
    """Ensure that a definition can be evaluated with width and height as positional
    arguments."""

    @ar.definition()
    def Base(width, height):
        return width + height

    assert Base()(4, 4) == 8

    @ar.definition()
    def Derived(height, base: Base):
        return height - base

    assert Derived()(2, 4) == -2


def test_derived_definition_eval_kwargs():
    """Ensure that a definition can be evaluted with inputs provided as keyword
    arguments"""

    @ar.definition()
    def Base(width, height):
        return width + height

    assert Base()(width=4, height=4) == 8

    @ar.definition()
    def Derived(height, base: Base):
        return height - base

    assert Derived()(height=4, base=4) == 0


@py.test.mark.parametrize(
    "op,fn",
    [
        (ar.Definition.OP_ADD, lambda a, b: a + b),
        (ar.Definition.OP_AND, lambda a, b: a & b),
        (ar.Definition.OP_DIV, lambda a, b: a / b),
        (ar.Definition.OP_FLOORDIV, lambda a, b: a // b),
        (ar.Definition.OP_LSHIFT, lambda a, b: a << b),
        (ar.Definition.OP_MATMUL, lambda a, b: a @ b),
        (ar.Definition.OP_MOD, lambda a, b: a % b),
        (ar.Definition.OP_MUL, lambda a, b: a * b),
        (ar.Definition.OP_OR, lambda a, b: a | b),
        (ar.Definition.OP_POW, lambda a, b: a ** b),
        (ar.Definition.OP_RSHIFT, lambda a, b: a >> b),
        (ar.Definition.OP_SUB, lambda a, b: a - b),
        (ar.Definition.OP_XOR, lambda a, b: a ^ b),
    ],
)
def test_definition_binary_operation_not_supported_other_objects(op, fn):
    """Ensure that we throw a sensible error if a user tries to perform an operation
    with an object that is not supported."""

    @ar.definition()
    def Defn():
        pass

    defn = Defn()
    op_name = op.capitalize().replace("_", " ")
    message = "{} is not supported between {} and {}"

    with py.test.raises(TypeError) as err:
        fn(defn, 1)

    assert message.format(op_name, "Defn[Any]", "int") == str(err.value)

    with py.test.raises(TypeError) as err:
        fn(1, defn)

    assert message.format(op_name, "int", "Defn[Any]") == str(err.value)
