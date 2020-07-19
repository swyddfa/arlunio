from typing import Any

import py.test

import arlunio as ar
from arlunio import DefnInput


@ar.definition
def Const():
    return 1


@ar.definition
def Base(width: int, height: int):
    return 2


@ar.definition
def Cuboid(width: int, color: str, base: Base):
    return 3


@ar.definition()
def Tunnel(base: Base, length: int):
    return 4


class TestDefinition:
    """Tests around the basic properties of a definition"""

    def test_name(self):
        """Ensure that the returned definition keeps the name of the decorated
        function."""

        @ar.definition
        def Circle():
            pass

        assert Circle.__name__ == "Circle"

    def test_module(self):
        """Ensure that the returned definition reports its module as the one it was
        defined in."""

        @ar.definition()
        def Circle():
            pass

        assert Circle.__module__ == "tests.test_definition"

    def test_constant(self):
        """Ensure that we can define a constant definition."""

        @ar.definition()
        def Constant():
            return 1

        const = Constant()
        assert const() == 1

    def test_param_missing_annotation(self):
        """Ensure that we require parameters to carry a type annotation"""

        with py.test.raises(TypeError) as err:

            @ar.definition()
            def Width(width):
                return width + 1

        assert "Missing type annotation" in str(err.value)
        assert "width" in str(err.value)

    def test_errors_with_pos_args(self):
        """Ensure that if a definition is called with positional args a helpful
        error message is thrown."""

        @ar.definition
        def Height(height: int):
            return height

        h = Height()

        with py.test.raises(TypeError) as err:
            h(12)

        assert "must be passed as keyword arguments" in str(err.value)

    def test_simple_param(self):
        """Ensure that we can define a parameter that takes a simple parameter."""

        @ar.definition
        def Height(height: int):
            return height - 1

        h = Height()
        assert h(height=100) == 99

    def test_attributes(self):
        """Ensure that we can define a definition that takes a number of attributes."""

        @ar.definition()
        def Param(*, offset=0):
            return 2 - offset

        p = Param()
        assert p() == 2

        q = Param(offset=2)
        assert q() == 0

    def test_produces_any(self):
        """Ensure that a definition without a return annotation reports its return type
        as :code:`Any`."""

        @ar.definition()
        def Param():
            pass

        assert Param.produces() == Any
        assert Param().produces() == Any

    def test_produces(self):
        """Ensure that a definition reports what type it returns as declared by its
        return annotation."""

        @ar.definition()
        def Param() -> int:
            return 1

        assert Param.produces() == int
        assert Param().produces() == int


class TestDefinitionInputs:
    """Tests relating to definition inputs."""

    def test_constant_defn(self):
        """Defns that don't define any inputs should return an empty dict."""

        assert Const.inputs() == {}
        assert Const().inputs() == {}

    def test_simple_defn(self):
        """Ensure that all explicitly defined definitions are reported."""

        expected = {
            "width": DefnInput(name="width", dtype=int, inherited=False),
            "height": DefnInput(name="height", dtype=int, inherited=False),
        }

        assert Base.inputs() == expected
        assert Base().inputs() == expected

    def test_simple_derived(self):
        """Any inputs from base definitions should also be exposed by default, but
        marked as being inherited."""

        expected = {
            "length": DefnInput(name="length", dtype=int, inherited=False),
            "width": DefnInput(name="width", dtype=int, inherited=True, sources=[Base]),
            "height": DefnInput(
                name="height", dtype=int, inherited=True, sources=[Base]
            ),
        }

        assert Tunnel.inputs() == expected
        assert Tunnel().inputs() == expected

    def test_simple_derived_inhertited_false(self):
        """Ensure that we can ask only for the inputs that have been directly declared
        on the definition."""

        expected = {"length": DefnInput(name="length", dtype=int, inherited=False)}

        assert Tunnel.inputs(inherited=False) == expected
        assert Tunnel().inputs(inherited=False) == expected

    def test_shadowed_inputs(self):
        """Ensure that any inputs that are both explicitly declared and carried on a
        base definition are marked as not being inherited."""

        expected = {
            "width": DefnInput(name="width", dtype=int, inherited=False),
            "color": DefnInput(name="color", dtype=str, inherited=False),
            "height": DefnInput(
                name="height", dtype=int, inherited=True, sources=[Base]
            ),
        }

        assert Cuboid.inputs() == expected
        assert Cuboid().inputs() == expected

    def test_shadowed_inputs_many_sources(self):
        """Ensure that any inputs inherited from multiple sources are captured as
        such."""

        @ar.definition
        def ADefn(b: Base, c: Cuboid):
            pass

        expected = {
            "width": DefnInput(
                name="width", dtype=int, inherited=True, sources=[Base, Cuboid]
            ),
            "height": DefnInput(
                name="height", dtype=int, inherited=True, sources=[Base, Cuboid]
            ),
            "color": DefnInput(
                name="color", dtype=str, inherited=True, sources=[Cuboid]
            ),
        }

        assert ADefn.inputs() == expected
        assert ADefn().inputs() == expected

    def test_report_conflicting_inputs(self):
        """Ensure that if a definition declares an input that conflicts with an
        inherited one an appropriate error is raised."""

        with py.test.raises(TypeError) as err:

            @ar.definition
            def BadDefinition(width: str, base: Base):
                pass

        assert "conflicts with" in str(err.value)
        assert "'width'" in str(err.value)
        assert "'Base'" in str(err.value)

    def test_report_conflicting_bases(self):
        """Ensure that if a definition includes bases that have conflicting inputs
        an appropriate error is raised."""

        @ar.definition
        def Other(width: str):
            pass

        with py.test.raises(TypeError) as err:

            @ar.definition
            def Derived(b: Base, o: Other):
                pass

        assert "conflicts with" in str(err.value)
        assert "'width'" in str(err.value)
        assert "'Base'" in str(err.value)


class TestDerivedDefinitions:
    """Tests related to deriving definitions."""

    def test_derivation(self):
        """Ensure that we can derive a definition that's based on other definitions."""

        @ar.definition()
        def Adder(width: int, height: int):
            return height + width

        @ar.definition()
        def Subber(a: Adder):
            return a - 2

        s = Subber()
        assert s(width=1, height=1) == 0
        assert s(width=1, height=2) == 1

    def test_attributes(self):
        """Ensure that the attributes method only exposes the attributes that are
        directly defined on the definition by default."""

        @ar.definition
        def Base(width: int, height: int, *, a: int = 1, b=2):
            return 3

        expected = {
            "a": ar.DefnAttribute(name="a", dtype=int, inherited=False, default=1),
            "b": ar.DefnAttribute(name="b", inherited=False, default=2),
        }

        assert Base().attributes() == expected

        @ar.definition
        def Derived(base: Base, *, b=3, d: float = 4.0):
            return 5

        expected = {
            "b": ar.DefnAttribute(name="b", inherited=False, default=3),
            "d": ar.DefnAttribute(name="d", dtype=float, inherited=False, default=4.0),
        }

        assert Derived().attributes() == expected

    def test_inherited_attributes(self):
        """Ensure that the attributes method with the inherited flag exposes all
        available attributes on the definition."""

        @ar.definition
        def Base(width: int, height: int, *, a: int = 1, b=2):
            return 3

        expected = {
            "a": ar.DefnAttribute(name="a", dtype=int, inherited=False, default=1),
            "b": ar.DefnAttribute(name="b", inherited=False, default=2),
        }

        assert Base().attributes(inherited=True) == expected

        @ar.definition()
        def Derived(base: Base, *, b=3, d: float = 4.0):
            return 5

        expected = {
            "a": ar.DefnAttribute(name="a", dtype=int, inherited=True, default=1),
            "b": ar.DefnAttribute(name="b", inherited=False, default=3),
            "d": ar.DefnAttribute(name="d", dtype=float, inherited=False, default=4.0),
        }

        assert Derived().attributes(inherited=True) == expected

    def test_values(self):
        """Ensure that the values method by default only exposes the values of the
        attributes that were directly declared."""

        @ar.definition
        def Base(width: int, height: int, *, a=1, b=2):
            return 3

        assert {"a": 1, "b": 2} == Base().values()

        @ar.definition()
        def Derived(base: Base, *, b=3, d=4):
            return 5

        assert {"b": 3, "d": 4} == Derived().values()

    def test_inherited_values(self):
        """Ensure that the values method with the inherited flag exposes all attribute
        values."""

        @ar.definition
        def Base(width: int, height: int, *, a=1, b=2):
            return 3

        assert {"a": 1, "b": 2} == Base().values(inherited=True)

        @ar.definition()
        def Derived(base: Base, *, b=3, d=4):
            return 5

        assert {"a": 1, "b": 3, "d": 4} == Derived().values(inherited=True)

    def test_eval_kwargs(self):
        """Ensure that a definition can be evaluted with inputs provided as keyword
        arguments"""

        @ar.definition()
        def Base(width: int, height: int):
            return width + height

        assert Base()(width=4, height=4) == 8

        @ar.definition()
        def Derived(height: int, base: Base):
            return height - base

        assert Derived()(height=4, base=4) == 0

    def test_exposes_attributes(self):
        """Ensure that any attributes on base definitions are exposed on the derived
        definition."""

        @ar.definition()
        def Base(width: int, height: int, *, offset=0):
            return offset

        @ar.definition()
        def Derived(b: Base, *, start=1):
            return start - b

        d = Derived()
        d(width=1, height=1) == 1

        d = Derived(start=5, offset=-1)
        d(width=1, height=1) == 6

    @py.test.mark.parametrize(
        "defn,expected",
        [(Base, {}), (Tunnel, {"base": ar.DefnBase(name="base", defn=Base)})],
    )
    def test_bases(self, defn, expected):
        """Ensure that any bases a definition is derived from is exposed."""

        assert defn.bases() == expected
        assert defn().bases() == expected


class TestDefinitionOperations:
    """Tests related to definition operations."""

    @py.test.mark.parametrize(
        "op,fn",
        [
            (ar.Defn.OP_ADD, lambda a, b: a + b),
            (ar.Defn.OP_AND, lambda a, b: a & b),
            (ar.Defn.OP_DIV, lambda a, b: a / b),
            (ar.Defn.OP_FLOORDIV, lambda a, b: a // b),
            (ar.Defn.OP_LSHIFT, lambda a, b: a << b),
            (ar.Defn.OP_MATMUL, lambda a, b: a @ b),
            (ar.Defn.OP_MOD, lambda a, b: a % b),
            (ar.Defn.OP_MUL, lambda a, b: a * b),
            (ar.Defn.OP_OR, lambda a, b: a | b),
            (ar.Defn.OP_POW, lambda a, b: a ** b),
            (ar.Defn.OP_RSHIFT, lambda a, b: a >> b),
            (ar.Defn.OP_SUB, lambda a, b: a - b),
            (ar.Defn.OP_XOR, lambda a, b: a ^ b),
        ],
    )
    def test_binary_operation_not_supported_other_objects(self, op, fn):
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

    def test_operator_missing_attributes(self):
        """Ensure that an operator defines an :code:`a` and :code:`b` attribute"""

        with py.test.raises(TypeError) as err:

            @ar.definition(operation="op")
            def Op(width: int, height: int):
                pass

        assert "must define 2 attributes" in str(err.value)
        assert "'a'" in str(err.value)
        assert "'b'" in str(err.value)

    def test_operator_missing_annotation(self):
        """Ensure that an operator defines a type annotation for each input"""

        with py.test.raises(TypeError) as err:

            @ar.definition(operation="op")
            def OpA(width: int, height: int, *, a=1, b: int = 2):
                pass

        assert "missing a valid type annotation" in str(err.value)
        assert "'a'" in str(err.value)

        with py.test.raises(TypeError) as err:

            @ar.definition(operation="op")
            def OpB(width: int, height: int, *, a: int = 1, b=2):
                pass

        assert "missing a valid type annotation" in str(err.value)
        assert "'b'" in str(err.value)

    def test_operator_existing_definition(self):
        """Ensure that if an existing operator has already been defined an error is
        thrown."""

        operator_pool = {}

        @ar.definition(operation="op", operator_pool=operator_pool)
        def Op(width: int, height: int, *, a: int = 0, b: int = 0):
            pass

        with py.test.raises(TypeError) as err:

            @ar.definition(operation="op", operator_pool=operator_pool)
            def OpDuplicate(width: int, height: int, *, a: int = 0, b: int = 0):
                pass

        assert "has already been defined" in str(err.value)
