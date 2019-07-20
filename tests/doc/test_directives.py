import py.test
import stylo as st
from docutils.statemachine import StringList
from stylo.doc.directives import format_error, load_shape


class TestLoadShape:
    """Tests for the :code:`load_shape` function."""

    def test_bad_module_name(self):
        """Ensure that a :code:`ModuleNotFoundError` is raised if a bad module
        name is given."""

        with py.test.raises(ModuleNotFoundError) as err:
            load_shape("badmod.Circle")

        assert "badmod" in str(err.value)

    def test_bad_module_path(self):
        """Ensure that a :code:`ModuleNotFoundError` is raised if a bad submodule
        name is given."""

        with py.test.raises(ModuleNotFoundError) as err:
            load_shape("stylo.badmod.Circle")

        assert "stylo.badmod" in str(err.value)

    def test_bad_object_name(self):
        """Ensure that an :code:`AttributeError` is raised if an object name is
        given that does not exist"""

        with py.test.raises(AttributeError) as err:
            load_shape("stylo.lib.basic.BadShapeName")

        assert "stylo.lib.basic" in str(err.value)
        assert "BadShapeName" in str(err.value)

    def test_bad_object_type(self):
        """Ensure that a :code:`TypeError` is raised if an object is not a shape."""

        with py.test.raises(TypeError) as err:
            load_shape("stylo.doc.directives.AutoShapeDirective")

        assert "is not a shape" in str(err.value)
        assert "AutoShapeDirective" in str(err.value)

    def test_load_shape(self):
        """Ensure that we can load a shape."""

        circle = load_shape("stylo.lib.basic.Circle")
        assert issubclass(circle, st.Shape)


class TestFormatError:
    """Tests for the :code:`format_error` function."""

    def test_formatter(self):

        err = "\n".join(
            [
                "Traceback (most recent call last):",
                '   File "<stdin>", line 1, in <module>',
                "ZeroDivisionError: division by zero",
            ]
        )
        content = format_error("Unable to perform :code:`2 / 0`", err)

        assert isinstance(content, StringList)

        actual = list(content)
        expected = [
            ".. error::",
            "",
            "   Unable to perform :code:`2 / 0`::",
            "",
            "      Traceback (most recent call last):",
            '         File "<stdin>", line 1, in <module>',
            "      ZeroDivisionError: division by zero",
            "",
        ]

        assert expected == actual
